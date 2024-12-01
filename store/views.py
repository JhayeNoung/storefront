from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status, mixins
from .models import Product, Review, Cart, CartItem, Customer, Order, OrderItem
from .serializers import ProductSerializer, ReviewModelSerializer, CartItemSerializer, CartSerializer, AddCartItemSerializer, UpdateItemSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer, CreateOrderSerializer, UpdateOrderSerializer
from .filters import ProductFilter
from .paginations import ProductPagination
from .permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all() # many(product) -> one(collection)
    serializer_class = ProductSerializer

    # filtering
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    pagination_class = ProductPagination
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'unit_price ']

    # permission
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    # custom DELETE method for instance.orderitem_set.count() > 0
    def destroy(self, request, pk):
        instance = get_object_or_404(Product, pk=pk)
        if instance.orderitem_set.count() > 0:
            return Response(data="Cannot delete product with associated order items.", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer

    # get product_pk from url and give to serializer.context['product_id'] ( /domains/{domain_pk}/nameservers/ )
    def get_serializer_context(self):
      """
      Extra context provided to the serializer class.
      """
      return {
          'product_id': self.kwargs['product_pk'] 
      }
    

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('cartitem').all()
    serializer_class = CartSerializer

    http_method_names = ['get', 'post', 'delete']
  

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()

    # we will not allow PUT method
    # http_method_names attribute is from the base class of Django, View
    http_method_names = ['get', 'post', 'patch', 'delete']

    # for POST method choose AddCartItemSerializer, for GET and ATNOTHER choose CartItemSerializer
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateItemSerializer
        return CartItemSerializer

    # get cart_pk from url and give to serializer.context['cart_id'] ( /domains/{domain_pk}/nameservers/ )
    def get_serializer_context(self):
        return {
            'cart_id': self.kwargs['cart_pk']
        }
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [IsAdminUser]

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.request.method == "GET":
    #         return [AllowAny()] # AllowAny() return True
    #     return [IsAuthenticated()]
    
    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('Here is the history')
    
    '''
    adding extra action 'me', REST framework will provide routes /me/

    https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
    '''
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        '''must give JWT token, then request object will inclued user object'''
        # extract tuple
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)# get_or_create returns a tuple of (object, created), where object is the retrieved or created object and created is a boolean
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)  
        if request.method == 'PUT':
            # Update the existing customer object
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    # if user is admin get all, if not, only its authenticated user
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        
        (customer_id, created) = Customer.objects.only('id').get_or_create(user_id=self.request.user.id) # find customer profile with the user_id
        return Order.objects.filter(customer_id=customer_id) # get order for this customer profile


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


