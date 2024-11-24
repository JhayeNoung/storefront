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


# for POST method
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    # if invalid product_id, raise custom error message
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID')
        return value
    
    def create(self, validated_data):
        """
        this method is essentially just:
            return ExampleModel.objects.create(**validated_data)
        """
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            # update
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            return cart_item
        except CartItem.DoesNotExist:
            # create new
            return CartItem.objects.create(cart_id=cart_id, **validated_data  )


# for GET and ALL method
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, cartitem):
        return cartitem.product.unit_price * cartitem.quantity


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cartitem = CartItemSerializer(many=True) # many(cartitem) -> one(cart)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'cartitem','total_price']

    def get_total_price(self, cart):
        return sum([item.product.unit_price * item.quantity for item in cart.cartitem.all()])


    


      
