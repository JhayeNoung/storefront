from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views
'''
/domains/ <- Domains list
/domains/{pk}/ <- One domain, from {pk}
/domains/{domain_pk}/nameservers/ <- Nameservers of domain from {domain_pk}
/domains/{domain_pk}/nameservers/{pk} <- Specific nameserver from {pk}, of domain from {domain_pk}
'''
router = DefaultRouter()
router.register('product', views.ProductViewSet)
router.register('cart', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet)

product_router = routers.NestedSimpleRouter(router, 'product', lookup='product')
product_router.register('review', views.ReviewViewSet, basename='review')

cart_router = routers.NestedSimpleRouter(router, 'cart', lookup='cart')
cart_router.register('cart-items', views.CartItemViewSet, basename='cartitems')

order_router = routers.NestedSimpleRouter(router, 'orders', lookup='orders')
order_router.register('order-items', views.CartItemViewSet, basename='orderitems')

urlpatterns = [
  path('', include(router.urls)),
  path('', include(product_router.urls)),
  path('', include(cart_router.urls)),
  path('', include(order_router.urls)),
]

# 'basename' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/
