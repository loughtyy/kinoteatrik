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
path('api-auth/', include('rest_framework.urls')),
path('Products/<int:pk>/name/', views.ProductsHighlight.as_view()),
path('', views.api_root),
]
