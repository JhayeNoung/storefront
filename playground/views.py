from django.shortcuts import get_object_or_404, render
from store.models import Product, Review
from store.serializers import ProductSerializer, ReviewModelSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

# Create your views here.
def demo(request):
    query_set = Product.objects.all()
    list(query_set)
    list(query_set)
    # product_obj = Product.objects.prefetch_related('promotions')
    return render(request, 'demo.html', {'name': 'jhaye', 'query_set':query_set})


# Generic Views
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def destroy(self, request, pk):
        instance = get_object_or_404(Product, pk=pk)
        if instance.orderitem_set.count() > 0:
            return Response(data="Cannot delete product with associated order items.", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# ViewSet
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def destroy(self, request, pk):
        instance = get_object_or_404(Product, pk=pk)
        if instance.orderitem_set.count() > 0:
            return Response(data="Cannot delete product with associated order items.", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewModelSerializer
    queryset = Review.objects.all()