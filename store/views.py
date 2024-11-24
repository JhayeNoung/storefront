from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from .models import Product, Review, Cart, CartItem
from .serializers import ProductSerializer, ReviewModelSerializer, CartItemSerializer, CartSerializer, AddCartItemSerializer
from .filters import ProductFilter
from .paginations import ProductPagination

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
  

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()

    # for POST method choose AddCartItemSerializer, for GET and ATNOTHER choose CartItemSerializer
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer

    # get cart_pk from url and give to serializer.context['cart_id'] ( /domains/{domain_pk}/nameservers/ )
    def get_serializer_context(self):
        return {
            'cart_id': self.kwargs['cart_pk']
        }