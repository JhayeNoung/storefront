from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework_nested import routers
'''
/domains/ <- Domains list
/domains/{pk}/ <- One domain, from {pk}
/domains/{domain_pk}/nameservers/ <- Nameservers of domain from {domain_pk}
/domains/{domain_pk}/nameservers/{pk} <- Specific nameserver from {pk}, of domain from {domain_pk}
'''
router = routers.SimpleRouter()
router.register('product', views.ProductViewSet)
router.register('cart', views.CartViewSet)

product_router = routers.NestedSimpleRouter(router, 'product', lookup='product')
product_router.register('review', views.ReviewViewSet, basename='product-review')

cart_router = routers.NestedSimpleRouter(router, 'cart', lookup='cart')

urlpatterns = [
  path('', include(router.urls)),
  path('', include(product_router.urls)),
  path('', include(cart_router.urls)),
]

# 'basename' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/
