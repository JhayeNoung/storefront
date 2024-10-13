from django.shortcuts import render
from django.db.models import F, Count, Value, Func
from store.models import Product, OrderItem, Order, Customer
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem, TaggedItemManager


# Create your views here.
def say_hello(request):
    query_set = TaggedItem.objects.get_tags_for(Product, 1)
    # product_obj = Product.objects.prefetch_related('promotions')
    return render(request, 'hello.html', {'name': 'jhaye', 'query_set':query_set})