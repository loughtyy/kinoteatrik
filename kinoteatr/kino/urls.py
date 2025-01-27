from django.urls import path
from .views import *

app_name="kino"

urlpatterns = [path('products/', ProductView.as_view()),]