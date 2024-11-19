from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', views.ProductViewSet, basename='product')
router.register('review', views.ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    
    path('product-list/', views.ProductList.as_view()),
    path('product-list/<int:pk>', views.ProductDetail.as_view()),
]
