from rest_framework import serializers
from .models import Products

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
    def create(self, validated_data):
     return Products.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.studios = validated_data.get('studios', instance.studios)
        instance.status = validated_data.get('status', instance.status)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.quality = validated_data.get('quality', instance.quality)
        instance.views = validated_data.get('views', instance.views)
        instance.save()
        return instance