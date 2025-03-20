from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='product-highlight', format='html')
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
            'products',
            'highlight'
        ]
        owner = serializers.ReadOnlyField(source='owner.username')
       

        
class SessionSerializer(serializers.ModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='session-highlight', format='html', lookup_field='pk')

    class Meta:
        model = Session
        fields = [
            'id',
            'film',
            'session_time',
            'hall_number',
            'owner',
            'highlight'  
        ]
        owner = serializers.ReadOnlyField(source='owner.username')


class TicketSerializer(serializers.ModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='ticket-highlight', format='html', lookup_field='pk')

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


class UserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Products.objects.all())
    highlight = serializers.HyperlinkedIdentityField(view_name='users-highlight', format='html', lookup_field='pk')

    class Meta:
        model = User
        fields = ['id', 
                  'username', 
                  'products',
                  'highlight']
    
