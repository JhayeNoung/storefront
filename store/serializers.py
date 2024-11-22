from rest_framework import serializers
from .models import Product, Review, Cart, CartItem

class ReviewModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = ['id','date','name','description']

  def create(self, validated_data):
    product_id = self.context['product_id']
    return Review.objects.create(product_id=product_id, **validated_data)
  
class ProductSerializer(serializers.ModelSerializer):
  price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
  collection = serializers.StringRelatedField() # a product has under one collection, a collection has many product under it

  class Meta:
    model = Product
    fields = ['id', 'title', 'price', 'description', 'collection']


class CartItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = CartItem
    fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
  id = serializers.UUIDField(read_only=True)
  items = CartItemSerializer

  class Meta:
    model = Cart
    fields = ['id', 'created_at', 'items']


    
