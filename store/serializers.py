from rest_framework import serializers
from .models import Product, Review, Cart, CartItem, Collection

class ReviewModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = ['id','date','name','description']

  def create(self, validated_data):
    product_id = self.context['product_id']
    return Review.objects.create(product_id=product_id, **validated_data)
  
class ProductSerializer(serializers.ModelSerializer):
  price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price') # source to 'unit_price' coz name change as 'price'
  collection_id = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all(), source='collection')  # Accept only collection ID

  class Meta:
    model = Product
    fields = ['id', 'title', 'price', 'description', 'inventory', 'collection_id']


class CartItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = CartItem
    fields = ['id', 'product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
  id = serializers.UUIDField(read_only=True)
  items = CartItemSerializer(many=True) # many(cartitem) -> one(cart)
  total_price = serializers.SerializerMethodField()

  class Meta:
    model = Cart
    fields = ['id', 'created_at', 'items','total_price']

  def get_total_price(self, cart):
    return sum([item.product.unit_price * item.quantity for item in cart.items.all()])


  


    
