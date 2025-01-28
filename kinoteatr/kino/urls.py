from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'products', ProductsViewSet, basename='products')
# urlpatterns = router.urls

app_name = "kino"
urlpatterns = [
 path('products/', ProductsViewSet.as_view()),
 path('products/<int:pk>', SingleProductView.as_view()),
]