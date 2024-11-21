from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register('product', views.ProductViewSet)

product_router = routers.NestedSimpleRouter(router, 'product', lookup='product')
product_router.register('review', views.ReviewViewSet, basename='product-review')

urlpatterns = [
  path('', include(router.urls)),
  path('', include(product_router.urls)),
]

# 'basename' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/
