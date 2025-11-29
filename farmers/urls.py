from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProduceListingViewSet, MarketPriceViewSet, create_listing, edit_listing, delete_listing, listings_list

from buyers.views import OrderViewSet

router = DefaultRouter()
router.register(r'listings', ProduceListingViewSet)
router.register(r'market-prices', MarketPriceViewSet)
router.register(r'orders', OrderViewSet, basename='farmer-orders')

urlpatterns = [
    path('', include(router.urls)),
]

# Template URLs (accessed via /farmers/)
template_urlpatterns = [
    path('listings/', listings_list, name='farmers_listings'),
    path('listings/create/', create_listing, name='farmers_create_listing'),
    path('listings/<int:pk>/edit/', edit_listing, name='farmers_edit_listing'),
    path('listings/<int:pk>/delete/', delete_listing, name='farmers_delete_listing'),
]
