from django.shortcuts import render
from django.db.models import F, Count, Value, Func
from store.models import Product, OrderItem, Order, Customer

# Create your views here.
def say_hello(request):
    query_set = Customer.objects.annotate(orders_count=Count('order'))
    # product_obj = Product.objects.prefetch_related('promotions')
    return render(request, 'hello.html', {'name': 'jhaye', 'query_set':query_set})