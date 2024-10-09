from django.shortcuts import render
from store.models import Product, OrderItem

# Create your views here.
def say_hello(request):
    query_set = Product.objects.values('id', 'title', 'collection__title').filter(collection__id=1).order_by('title')[:5]
    product_obj = Product.objects.get(pk=1)
    # product_obj = Product.objects.all()
    return render(request, 'hello.html', {'name': 'jhaye', 'products':list(query_set), 'product_obj':product_obj})