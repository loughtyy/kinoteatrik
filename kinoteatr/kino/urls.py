from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'sessions', SessionViewSet, basename='sessions')
router.register(r'tickets', TicketViewSet, basename='tickets')
urlpatterns = router.urls
