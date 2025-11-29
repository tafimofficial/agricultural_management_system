from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, filters
from .models import ProduceListing, MarketPrice
from .serializers import ProduceListingSerializer, MarketPriceSerializer

class IsFarmerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'farmer'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.farmer == request.user

class ProduceListingViewSet(viewsets.ModelViewSet):
    queryset = ProduceListing.objects.filter(is_active=True)
    serializer_class = ProduceListingSerializer
    permission_classes = [IsFarmerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'location', 'description']

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

class MarketPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MarketPrice.objects.all().order_by('-date')
    serializer_class = MarketPriceSerializer
    permission_classes = [permissions.AllowAny]


@login_required
def create_listing(request):
    if request.method == 'POST':
        listing = ProduceListing.objects.create(
            farmer=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            quantity=request.POST.get('quantity'),
            location=request.POST.get('location'),
            image=request.FILES.get('image') if 'image' in request.FILES else None
        )
        return redirect('dashboard')
    return render(request, 'farmers/create_listing.html')

@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(ProduceListing, pk=pk, farmer=request.user)
    if request.method == 'POST':
        listing.title = request.POST.get('title')
        listing.description = request.POST.get('description')
        listing.price = request.POST.get('price')
        listing.quantity = request.POST.get('quantity')
        listing.location = request.POST.get('location')
        if 'image' in request.FILES:
            listing.image = request.FILES.get('image')
        listing.save()
        return redirect('dashboard')
    return render(request, 'farmers/edit_listing.html', {'listing': listing})

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(ProduceListing, pk=pk, farmer=request.user)
    if request.method == 'POST':
        listing.delete()
        return redirect('dashboard')
    return render(request, 'farmers/delete_confirm.html', {'listing': listing})

@login_required
def listings_list(request):
    listings = ProduceListing.objects.filter(farmer=request.user).order_by('-created_at')
    return render(request, 'farmers/listings.html', {'listings': listings})
