from rest_framework import serializers
from .models import Order, OrderItem
from farmers.models import ProduceListing
from decimal import Decimal

class OrderItemSerializer(serializers.ModelSerializer):
    listing_title = serializers.ReadOnlyField(source='listing.title')

    class Meta:
        model = OrderItem
        fields = ('id', 'listing', 'listing_title', 'quantity', 'price')
        read_only_fields = ('price',)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    buyer_name = serializers.ReadOnlyField(source='buyer.username')

    class Meta:
        model = Order
        fields = ('id', 'buyer', 'buyer_name', 'status', 'total_amount', 'created_at', 'items')
        read_only_fields = ('buyer', 'total_amount', 'created_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        buyer = self.context['request'].user
        
        # Remove buyer and status from validated_data
        validated_data.pop('buyer', None)
        validated_data.pop('status', None)
        
        # Calculate total and perform stock checks
        total_amount = Decimal('0.00') # Initialize as Decimal
        
        # Pre-process items to check stock and calculate total before creating order
        processed_items = []
        for item_data in items_data:
            listing = item_data['listing']
            quantity = Decimal(str(item_data['quantity'])) # Ensure quantity is Decimal
            
            if listing.quantity < quantity:
                raise serializers.ValidationError(f"Not enough stock for {listing.title}. Available: {listing.quantity}, Requested: {quantity}")
            
            total_amount += listing.price * quantity
            processed_items.append({
                'listing': listing,
                'quantity': quantity,
                'price': listing.price # Store price at time of order
            })
        
        order = Order.objects.create(buyer=buyer, total_amount=total_amount, **validated_data)
        
        for item_data in processed_items:
            listing = item_data['listing']
            quantity = item_data['quantity'] # Already a Decimal
            
            OrderItem.objects.create(
                order=order, 
                listing=listing, 
                quantity=quantity,
                price=item_data['price']
            )
            
            # Update listing quantity - convert to Decimal to avoid type mismatch
            listing.quantity = Decimal(str(listing.quantity)) - quantity
            listing.save()
            
        return order
