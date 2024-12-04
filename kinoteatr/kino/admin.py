from django.contrib import admin
from .models import *


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'duration', 'created_at')
    search_fields = ('name', 'description', 'studios')
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('film', 'session_time', 'hall_number')

