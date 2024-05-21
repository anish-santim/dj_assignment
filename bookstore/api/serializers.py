from rest_framework import serializers
from .models import Book , Category

class BookSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Book
        fields = ['id', 'title', 'year_published', 'author_name', 'price', 'category', 'stock']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
