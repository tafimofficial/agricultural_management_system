from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]

from .views import orders

# Template URLs (accessed via /buyers/)
template_urlpatterns = [
    path('orders/', orders, name='buyer_orders'),
]
