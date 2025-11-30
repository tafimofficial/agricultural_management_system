from django.core.management.base import BaseCommand
from produce.models import Produce
from django.utils import timezone
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populates the database with dummy produce data'

    def handle(self, *args, **kwargs):
        categories = ['Vegetable', 'Fruit', 'Grain', 'Other']
        names = {
            'Vegetable': ['Potato', 'Tomato', 'Onion', 'Carrot', 'Cabbage', 'Cauliflower', 'Spinach', 'Brinjal', 'Okra', 'Pumpkin'],
            'Fruit': ['Apple', 'Banana', 'Mango', 'Orange', 'Grape', 'Papaya', 'Guava', 'Watermelon', 'Pineapple', 'Litchi'],
            'Grain': ['Rice', 'Wheat', 'Corn', 'Barley', 'Millet', 'Oats'],
            'Other': ['Egg', 'Milk', 'Honey', 'Mushroom']
        }

        self.stdout.write('Deleting old data...')
        Produce.objects.all().delete()

        self.stdout.write('Creating 100 dummy produce items...')
        
        today = timezone.now().date()
        
        for i in range(100):
            category = random.choice(categories)
            name = random.choice(names[category])
            price = Decimal(random.uniform(10.0, 200.0)).quantize(Decimal('0.01'))
            
            # Randomly assign date to today or yesterday to test filtering
            # But user said "only show today data", so let's make most of them today
            # and some yesterday to verify they don't show up.
            if i < 80:
                date = today
            else:
                date = today - timezone.timedelta(days=1)

            Produce.objects.create(
                name=f"{name} {i+1}", # Unique names
                price_per_kg=price,
                category=category,
                date=date,
                # No image for dummy data, or could use a placeholder if available
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {Produce.objects.count()} produce items.'))
