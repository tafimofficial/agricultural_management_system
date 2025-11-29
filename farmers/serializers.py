from rest_framework import serializers
from .models import ProduceListing, MarketPrice

class ProduceListingSerializer(serializers.ModelSerializer):
    farmer_name = serializers.ReadOnlyField(source='farmer.username')
    farmer_id = serializers.ReadOnlyField(source='farmer.id')

    class Meta:
        model = ProduceListing
        fields = '__all__'
        read_only_fields = ('farmer', 'created_at')

class MarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPrice
        fields = '__all__'
