from django.urls import path

from . import views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('manage_books/', views.manage_books, name='manage_books'),
    path('login/', views.login_user, name='login_user'),
    path('create_user/', views.create_user, name='create_user'),
    path('logout/', views.logout_user, name='logout_user')
]