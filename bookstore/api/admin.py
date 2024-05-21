from django.contrib import admin

from django.contrib import admin
from .models import Category, Book, CartItem, CustomUser

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(CartItem)
admin.site.register(CustomUser)

