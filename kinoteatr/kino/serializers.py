from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
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
            'created_at'
        ]
class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = [
            'id',       
            'film',
            'session_time',
            'hall_number'
        ]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'id',            
            'user',
            'session',
            'created_at'
        ]