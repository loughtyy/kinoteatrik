from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='product-name', format='html')
    products = serializers.HyperlinkedRelatedField(many=True, view_name='products-detail', read_only=True)
    class Meta:
        model = Products
        fields = [
            'id',  
            'image',
            'name',
            'description',
            'type',
            'studios',
            'status',
            'duration',
            'quality',
            'views',
            'created_at',
            'owner',
            'products'
        ]
        owner = serializers.ReadOnlyField(source='owner.username')
       

        
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = [
            'id',       
            'film',
            'session_time',
            'hall_number',
            'owner'
        ]
        owner = serializers.ReadOnlyField(source='owner.username')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'id',            
            'user',
            'session',
            'created_at',
           
        ]
        user = serializers.ReadOnlyField(source='user.username')


class UserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Products.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username', 'products']
    
