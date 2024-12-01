from django.db import transaction
from rest_framework import serializers
from .signals import order_created
from .models import Product, Review, Cart, CartItem, Collection, Customer, Order, OrderItem

class ReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','date','name','description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    

class SimpleProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price') # source to 'unit_price' coz name change as 'price'

    class Meta:
        model = Product
        fields = ['id', 'title', 'price']

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price') # source to 'unit_price' coz name change as 'price'
    collection_id = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all(), source='collection')  # Accept only collection ID

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description', 'inventory', 'collection_id']


# for PATCH method
class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


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
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, cartitem):
        return cartitem.product.unit_price * cartitem.quantity


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cartitem = CartItemSerializer(many=True, read_only=True) # many(cartitem) -> one(cart)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'cartitem','total_price']

    def get_total_price(self, cart):
        return sum([item.product.unit_price * item.quantity for item in cart.cartitem.all()])


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ['id', 'user_id','phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(read_only=True, many=True)
    customer_id = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer_id', 'orderitems',]


'''give the cart_id of the user, and it will create OrderItem in the order, and delete the cart'''
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the given id was found .')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id
            
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']

            '''create new order of the authenticated customer profile'''
            customer= Customer.objects.get(user_id=self.context['user_id']) # find customer profile with the user_id
            order = Order.objects.create(customer=customer) # create order for this customer profile, return object

            '''create order items from the provided cart_id'''
            # get cart items from provided cart_id
            cart_items = CartItem.objects.filter(cart_id=cart_id) # return queryset

            # get cart item data and give to order item
            order_items = [
                OrderItem(
                    order = order,
                    product = item.product,
                    unit_price = item.product.unit_price,
                    quantity = item.quantity,
                ) for item in cart_items
            ]

            # creat order item
            OrderItem.objects.bulk_create(order_items)

            # delete the cart
            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__, order=order)

            return order
        

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
'''
store_cart
id created_at

store_cartitem
id quantity cart_id product_id

store_orderitem
id quantity unit_price product_id order_id


This method inserts the provided list of objects into the database in an efficient manner 
(generally only 1 query, no matter how many objects there are), and returns created objects as a list, 
in the same order as provided:
>>> objs = Entry.objects.bulk_create(
...     [
...         Entry(headline="This is a test"),
...         Entry(headline="This is only a test"),
...     ]
... )
'''