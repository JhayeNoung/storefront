from django.shortcuts import render
from store.models import Product

# Create your views here.
def say_hello(request):
    Product = Product.objects.all()
    return render(request, 'hello.html', {'name': 'jhaye'})