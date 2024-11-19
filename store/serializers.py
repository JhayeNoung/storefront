from rest_framework import serializers
from .models import Product, Collection

class ProductSerializer(serializers.ModelSerializer):
  price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
  collection = serializers.StringRelatedField() # a product has under one collection, a collection has many product under it

  class Meta:
    model = Product
    fields = ['id', 'title', 'price', 'description', 'collection']