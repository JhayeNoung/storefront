from django.urls import reverse
from rest_framework.test import APITestCase

'''
/domains/ <- Domains list
/domains/{pk}/ <- One domain, from {pk}
/domains/{domain_pk}/nameservers/ <- Nameservers of domain from {domain_pk}
/domains/{domain_pk}/nameservers/{pk} <- Specific nameserver from {pk}, of domain from {domain_pk}

https://www.django-rest-framework.org/api-guide/routers/#simplerouter
'''
from django.urls import reverse
from django.db import models
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status, serializers
from store.models import Product, Collection, Cart, CartItem
from store.serializers import CartItemSerializer
from store.views import CartItemViewSet
from uuid import uuid4

class ProductTest(APITestCase):
  def setUp(self):
      self.url = reverse('product-list')  # URL for the Product list endpoint

      collection = Collection.objects.create(title='hello')

      self.invalid_obj = { }  # Missing required fields
      self.valid_obj = {
          'title': 'Valid Product',
          'price': 100.00,
          'inventory': 10,
          'collection_id': collection.id,  # Use the existing Collection ID
      }

  def test_get_product(self):
      # Test GET request
      response = self.client.get(self.url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_post_product(self):
      # Test 400 Bad Request for invalid payload
      response = self.client.post(self.url, self.invalid_obj, format='json')
      self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

      # Test 201 Created for valid payload
      response = self.client.post(self.url, self.valid_obj, format='json')
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class CartItemTest(APITestCase):
    def setUp(self):
        # create cart data
        self.cart = Cart.objects.create(id=uuid4())
        
        # create product data
        collection = Collection.objects.create(title='hello')
        self.product = Product.objects.create(title='hello', unit_price=1, inventory=1, collection_id=collection.id)

        # create cart item
        self.cartItemView = CartItemViewSet()

        # url
        self.url = reverse('cartitem-list', kwargs={'cart_pk': self.cart.id})
        self.factory = APIRequestFactory()

    
    def test_get_serializer_context(self):
        # Simulate a request with cart_pk in kwargs
        request = self.factory.get('/cart/{}/cart-item/'.format(self.cart.id))
        self.cartItemView.request = request
        self.cartItemView.kwargs = {'cart_pk': str(self.cart.id)}
        print(self.cartItemView.__dict__)

        # Call the get_serializer_context method
        context = self.cartItemView.get_serializer_context()

        # Assert the context contains the correct cart_id
        self.assertEqual(context, {'cart_id': str(self.cart.id)})

    def test_post_cartItem(self):
        invalid_obj = { }
        valid_data = {
            'cart_id': self.cart.id,
            'product_id': self.product.id,
            'quantity': 1,
        }

        # test 400
        response = self.client.post(self.url, invalid_obj, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # test 201
        response = self.client.post(self.url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
