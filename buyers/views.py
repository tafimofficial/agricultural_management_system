from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'buyer':
            return Order.objects.filter(buyer=user)
        elif user.role == 'farmer':
            # Return orders that contain items from this farmer's listings
            return Order.objects.filter(items__listing__farmer=user).distinct()
        elif user.role == 'admin':
            return Order.objects.all()
        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def orders(request):
    return render(request, 'buyers/orders.html')
