from django.db import models
from enum import Enum


class DrivingStyle(Enum):
    VERY_EFFICIENT = 0.75
    EFFICIENT = 0.9
    REGULAR = 1.0
    AGGRESSIVE = 1.3043
    VERY_AGGRESSIVE = 1.5


class EVType(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    battery_capacity_kwh = models.FloatField()  # in kWh
    efficiency_kwh_per_km = models.FloatField()  # e.g., 0.2 kWh/km
    image_url = models.URLField()

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class Journey(models.Model):
    origin_latitude = models.FloatField(default=0)
    origin_longitude = models.FloatField(default=0)
    destination_latitude = models.FloatField(default=0)
    destination_longitude = models.FloatField(default=0)
    distance_km = models.FloatField(default=0)
    charge_used_kwh = models.FloatField(default=0)
    percentage_charge_used = models.FloatField(default=0)  # Removed the comma
    round_trip_charge_used_kwh = models.FloatField(
        default=0)  # Removed the comma
    round_trip_percentage_used = models.FloatField(
        default=0)  # Removed the comma
    ev_type = models.ForeignKey(EVType, on_delete=models.CASCADE, default=1)
    driving_style = models.CharField(max_length=20, default=DrivingStyle.REGULAR.name, choices=[(
        style.name, style.value) for style in DrivingStyle])

    def get_efficiency_multiplier(self):
        return DrivingStyle[self.driving_style].value

    def __str__(self):
        return f"Journey from ({self.origin_latitude}, {self.origin_longitude}) to ({self.destination_latitude}, {self.destination_longitude})"
