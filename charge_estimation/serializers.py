from rest_framework import serializers
from .models import EVType, Journey


class EVTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EVType
        fields = ['id', 'make', 'model', 'year', 'image_url', 'battery_capacity_kwh',
                  'efficiency_kwh_per_km']


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = '__all__'
