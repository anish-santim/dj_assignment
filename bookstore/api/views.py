from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from functools import wraps
from .validators import *
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import CustomUser, Category, Book, CartItem
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .serializers import BookSerializer
import json


def login_required_json(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not logged in'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def is_admin(user):
    return user.role == CustomUser.ADMIN


def custom_user_passes_test(test_func, login_url=None, redirect_field_name='next', custom_response=None):
    """
    Decorator for views that checks that the user passes the given test,
    returning a JSON response if the test fails.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not test_func(request.user):
                if custom_response:
                    return custom_response
                return JsonResponse({'error': 'You do not have permission to access this resource.'}, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# add to cart by admin or member
@csrf_exempt
@login_required_json
def add_to_cart(request, book_id):
    try:
        if request.method == "POST":
            book = get_object_or_404(Book, id=book_id, stock__gt=0)
            if not CartItem.objects.filter(user=request.user, book=book).exists():
                CartItem.objects.create(user=request.user, book=book)
            else:
                return JsonResponse({'message': 'Book already exists in cart!'}, status=409)
            return JsonResponse({'message': 'Book added to cart successfully'}, status=201)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# view cart by member or admin
@login_required_json
def view_cart(request):
    try:
        if request.method == 'GET':
            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                if item.is_expired():
                    item.delete()
            cart_items = CartItem.objects.filter(user=request.user)
            cart_items_data = [{'book_id': item.book.id, 'title': item.book.title,
                                'price': item.book.price} for item in cart_items]
            return JsonResponse({'cart_items': cart_items_data}, status=200)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# check out by member or admin
@csrf_exempt
@login_required_json
@transaction.atomic
def checkout(request):
    try:
        if request.method == 'PUT':
            cart_items = CartItem.objects.filter(user=request.user)
            expired_books, order_summary, out_of_stock = [], [], []
            if not cart_items:
                return JsonResponse({"message": "Cart is empty"}, status=200)
            with transaction.atomic():
                for item in cart_items:
                    if item.is_expired():
                        expired_books.append(item.book.title)
                    else:
                        book = Book.objects.get(id=item.book.id)
                        if book.stock:
                            order_summary.append(item.book.title)
                            book.stock -= 1
                            book.save()
                        else:
                            out_of_stock.append(item.book.title)
                    item.delete()
            response = {
                "message": "Transaction Summary",
                "order_summary": order_summary,
                "expired_books": expired_books,
                "out_of_stock": out_of_stock
            }
            return JsonResponse(response, status=200)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# manage categories by admin (CRUD)
@csrf_exempt
@login_required_json
@custom_user_passes_test(is_admin)
def manage_categories(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            validate_manage_category_post_payload(data)
            name = data.get('name')
            Category.objects.create(name=name)
            return JsonResponse({'message': 'Category created successfully'}, status=201)

        elif request.method == 'GET':
            categories = Category.objects.all()
            order_by = request.GET.get('order_by', 'name')
            categories = categories.order_by(order_by)
            page_number = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 10)
            paginator = Paginator(categories, page_size)
            page_obj = paginator.get_page(page_number)
            categories_data = [{'name': category.name}
                               for category in page_obj]
            return JsonResponse({'categories': categories_data}, status=200)

        elif request.method == 'PUT':
            data = json.loads(request.body)
            validate_manage_category_put_payload(data)
            old_name = data.get('old_name')
            new_name = data.get('new_name')
            try:
                category = Category.objects.get(name=old_name)
                category.name = new_name
                category.save()
                return JsonResponse({'message': 'Category updated successfully'}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)

        elif request.method == 'DELETE':
            data = json.loads(request.body)
            validate_manage_category_delete_payload(data)
            name = data.get('name')
            try:
                category = Category.objects.get(name=name)
                category.delete()
                return JsonResponse({'message': 'Category deleted successfully'}, status=200)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            return JsonResponse({'error': 'Category name can not be same'}, status=400)
        return JsonResponse({"error": str(e)}, status=400)


# manage books by admin (CRUD)
@csrf_exempt
@login_required_json
@custom_user_passes_test(is_admin)
def manage_books(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            validate_manage_books_post_payload(data)
            title = data.get('title')
            year_published = data.get('year_published')
            author_name = data.get('author_name')
            price = data.get('price')
            category_name = data.get('category')
            stock = data.get('stock')
            category = get_object_or_404(Category, name=category_name)
            Book.objects.create(title=title, year_published=year_published,
                                author_name=author_name, price=price, category=category, stock=stock)
            return JsonResponse({'message': 'Book added successfully'}, status=201)

        elif request.method == 'GET':
            books = Book.objects.all()
            order_by = request.GET.get('order_by', 'title')
            books = books.order_by(order_by)
            page_number = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 10)
            paginator = Paginator(books, page_size)
            page_obj = paginator.get_page(page_number)
            serializer = BookSerializer(page_obj, many=True)
            return JsonResponse({'books': serializer.data}, status=200)

        elif request.method == 'PUT':
            data = json.loads(request.body)
            validate_manage_books_put_payload(data)
            book_id = data.get('id')
            title = data.get('title')
            year_published = data.get('year_published')
            author_name = data.get('author_name')
            price = data.get('price')
            category_name = data.get('category')
            stock = data.get('stock')
            book = get_object_or_404(Book, id=book_id)
            if book.stock != stock:
                return JsonResponse({"error": "Stock cant be updated"}, status=400)
            book.title = title if title else book.title
            book.year_published = year_published if year_published else book.year_published
            book.author_name = author_name if author_name else book.author_name
            book.price = price if price else book.price
            book.category = get_object_or_404(
                Category, name=category_name) if category_name else book.category
            book.save()
            return JsonResponse({'message': 'Book updated successfully'}, status=200)

        elif request.method == 'DELETE':
            data = json.loads(request.body)
            validate_manage_books_delete_payload(data)
            title = data.get('title')
            book = get_object_or_404(Book, title=title)
            book.delete()
            return JsonResponse({'message': 'Book deleted successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            return JsonResponse({'error': 'Title cannot be same'}, status=400)
        return JsonResponse({"error": str(e)}, status=400)


# list all books that are in stock
def list_books(request):
    try:
        if request.method == 'GET':
            data = json.loads(request.body)
            validate_book_list_get_payload(data)
            category_names = data['categories']
            if category_names:
                books = Book.objects.filter(
                    category__name__in=category_names, stock__gt=0)
            else:
                books = Book.objects.filter(stock__gt=0)
            order_by = request.GET.get('order_by', 'title')
            books = books.order_by(order_by)
            page_number = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', 10)
            paginator = Paginator(books, page_size)
            page_obj = paginator.get_page(page_number)
            serializer = BookSerializer(page_obj, many=True)
            return JsonResponse({'books': serializer.data}, status=200)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# create new user
@require_POST
def create_user(request):
    try:
        data = json.loads(request.body)
        validate_post_login_payload(data)
        email = data.get('email')
        password = data.get('password')
        user = CustomUser(email=email)
        user.set_password(password)  # This hashes the password
        user.save()
        return JsonResponse({'message': "user created successfully"}, status=201)
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            return JsonResponse({'error': 'Email cannot be same'}, status=400)
        return JsonResponse({"error": str(e)}, status=400)

# login user
def login_user(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            validate_post_login_payload(data)
            email = data.get('email')
            password = data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid username or password'}, status=400)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# logout user
def logout_user(request):
    try:
        if request.method == 'POST':
            logout(request)
            return JsonResponse({'message': 'Logout Success'}, status=200)
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
