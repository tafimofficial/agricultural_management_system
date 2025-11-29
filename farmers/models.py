from django.db import models
from django.conf import settings

class ProduceListing(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.FloatField(help_text="Quantity in kg")
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='produce/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class MarketPrice(models.Model):
    crop_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.crop_name} - {self.price}"
