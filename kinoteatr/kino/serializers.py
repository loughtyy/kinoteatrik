from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework.validators import UniqueValidator

class ProductSerializer(serializers.ModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='products-detail', format='html') 
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
            'products',
            'highlight'
        ]

class SessionSerializer(serializers.ModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='sessions-detail', format='html') 

    class Meta:
        model = Session
        fields = [
            'id',
            'film',
            'session_time',
            'hall_number',
            'highlight'  
        ]

class TicketSerializer(serializers.ModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='tickets-detail', format='html') 

    class Meta:
        model = Ticket
        fields = [
            'id',
            'user',
            'session',
            'created_at',
            'highlight'  
        ]
        user = serializers.ReadOnlyField(source='user.username')

class ProductMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'image']

class UserSerializer(serializers.ModelSerializer):
    products = ProductMinimalSerializer(many=True, read_only=True) 
    highlight = serializers.HyperlinkedIdentityField(view_name='users-detail', format='html')  
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['id', 
                  'username', 
                  'products',
                  'highlight']