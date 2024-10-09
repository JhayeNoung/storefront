from django.shortcuts import render
from store.models import Product, OrderItem

# Create your views here.
def say_hello(request):
    query_set = Product.objects.filter(id__in=OrderItem.objects.values('product__id')).order_by('title')
    product_obj = Product.objects.get(pk=1)
    # product_obj = Product.objects.all()
    return render(request, 'hello.html', {'name': 'jhaye', 'products':list(query_set), 'product_obj':product_obj})