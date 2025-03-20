from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'sessions', SessionViewSet, basename='sessions')
router.register(r'tickets', TicketViewSet, basename='tickets')
router.register(r'users', UserViewSet, basename='users')
urlpatterns = router.urls

urlpatterns += [
path('', views.api_root),
path('api-auth/', include('rest_framework.urls')),
path('Products/<int:pk>/highlight/', views.ProductsHighlight.as_view(), name='product-highlight'), 
path('sessions/<int:pk>/highlight/', views.SessionHighlight.as_view(), name='session-highlight'), 
path('tickets/<int:pk>/highlight/', views.TicketHighlight.as_view(), name='ticket-highlight'),  
path('users/<int:pk>/highlight/', views.UserHighlight.as_view(), name='users-highlight')
]
