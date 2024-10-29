import csv
from django.core.management.base import BaseCommand
from charge_estimation.models import EVType
import os


class Command(BaseCommand):
    help = 'Import electric vehicle data from CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_file = os.path.join(os.path.dirname(__file__), 'car_data.csv')
        print("csv", csv_file)
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                EVType.objects.create(
                    make=row['make'],
                    model=row['model'],
                    year=int(row['year']),
                    battery_capacity_kwh=float(row['battery_capacity_kwh']),
                    efficiency_kwh_per_km=float(row['efficiency_kwh_per_km']),
                    image_url=row['image_url'].strip(
                        '"')  # Strip any extra quotes
                )
        self.stdout.write(self.style.SUCCESS(
            'Electric vehicle data imported successfully!'))
