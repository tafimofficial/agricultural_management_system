from django.db import models
from django.utils import timezone

class Produce(models.Model):
    CATEGORY_CHOICES = (
        ('Vegetable', 'Vegetable'),
        ('Fruit', 'Fruit'),
        ('Grain', 'Grain'),
        ('Other', 'Other'),
    )

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='produce_images/')
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Vegetable')

    def __str__(self):
        return f"{self.name} - {self.date}"
