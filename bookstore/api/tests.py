from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser, Category, Book, CartItem
import json
from .validators import *

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='user@example.com', password='password')
        self.admin_user = CustomUser.objects.create_user(email='admin@example.com', password='password', role=CustomUser.ADMIN)
        self.category = Category.objects.create(name='Fiction')
        self.book = Book.objects.create(title='Sample Book', year_published=2021, author_name='Author', price=10.00, category=self.category, stock=5)
        self.client.login(email='user@example.com', password='password')

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart', args=[self.book.id]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().book, self.book)
        self.assertEqual(self.book.stock, 5)

    def test_view_cart(self):
        CartItem.objects.create(user=self.user, book=self.book)
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Book', response.content.decode())

    def test_checkout(self):
        CartItem.objects.create(user=self.user, book=self.book)
        response = self.client.put(reverse('checkout'), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CartItem.objects.count(), 0)
        self.assertIn('Sample Book', response.json()['order_summary'])

    def test_manage_categories_post(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.post(reverse('manage_categories'), data=json.dumps({'name': 'New Category'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_manage_categories_get(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.get(reverse('manage_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Fiction', response.content.decode())

    def test_manage_categories_put(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.put(reverse('manage_categories'), data=json.dumps({'old_name': 'Fiction', 'new_name': 'Non-Fiction'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.get(id=self.category.id).name, 'Non-Fiction')

    def test_manage_categories_delete(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.delete(reverse('manage_categories'), data=json.dumps({'name': 'Fiction'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 0)

    def test_manage_books_post(self):
        self.client.login(email='admin@example.com', password='password')
        data = {
            'title': 'New Book',
            'year_published': 2022,
            'author_name': 'New Author',
            'price': 15.00,
            'category': 'Fiction',
            'stock': 10
        }
        response = self.client.post(reverse('manage_books'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 2)

    def test_manage_books_get(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.get(reverse('manage_books'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sample Book', response.content.decode())

    def test_manage_books_put(self):
        self.client.login(email='admin@example.com', password='password')
        data = {
            'id': self.book.id,
            'title': 'Updated Book',
            'year_published': 2023,
            'author_name': 'Updated Author',
            'price': 20.00,
            'category': 'Fiction',
            'stock': 5
        }
        response = self.client.put(reverse('manage_books'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_manage_books_delete(self):
        self.client.login(email='admin@example.com', password='password')
        response = self.client.delete(reverse('manage_books'), data=json.dumps({'title': 'Sample Book'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 0)

    def test_list_books(self):
        payload = json.dumps({'categories': ['Fiction']})
        response = self.client.generic('GET', reverse('list_books'), data=payload, content_type='application/json')
        self.assertIn('Sample Book', response.content.decode())

    def test_create_user(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        response = self.client.post(reverse('create_user'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_login_user(self):
        data = {
            'email': 'user@example.com',
            'password': 'password'
        }
        response = self.client.post(reverse('login_user'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful', response.content.decode())

    def test_logout_user(self):
        self.client.login(email='user@example.com', password='password')
        response = self.client.post(reverse('logout_user'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Logout Success', response.content.decode())