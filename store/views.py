from django.shortcuts import get_object_or_404
from .models import Product, Review
from .serializers import ProductSerializer, ReviewModelSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

# Create your views here.
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
    queryset = Review.objects.all()
    serializer_class = ReviewModelSerializer

    def get_serializer_context(self):
      """
      Extra context provided to the serializer class.
      """
      return {
          'product_id': self.kwargs['product_pk']
      }
    
      """
      In Django, self.kwargs is a dictionary that contains all the keyword arguments captured from the URL pattern.
	    These keyword arguments are defined in the URL configuration when using path converters, such as <int:product_pk>.
      """