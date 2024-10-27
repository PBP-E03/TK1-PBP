from django.core.management.base import BaseCommand
import csv
from resto.models import Restaurant  # Adjust this if your model is in the main app

class Command(BaseCommand):
    
    help = 'Imports restaurant data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        default_price = 50000  # Set your default price here

        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for i, row in enumerate(reader):
                if i >= 100:  # Limit to the first 100 rows
                    break
                price = int(row['price']) if row['price'] else default_price  # Use default if price is null
                Restaurant.objects.create(
                    name=row['restaurant_name'],
                    location=f"{row['city']} {row['district']}",
                    special_menu=row['unique_menu'],
                    price=price,
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported restaurant data.'))
