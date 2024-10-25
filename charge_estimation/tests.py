from django.test import TestCase
from .models import Journey, DrivingStyle, EVType


class JourneyModelTests(TestCase):
    def setUp(self):
        # Create an EVType instance
        self.ev_type = EVType.objects.create(
            make="Tesla",
            model="Model S",
            year=2013,
            battery_capacity_kwh=50,
            efficiency_kwh_per_km=0.143,
            image_url="http://example.com/tesla_model_s.jpg"
        )

    def test_default_driving_style(self):
        """Test that the default driving style is 'Regular'."""
        journey = Journey.objects.create(
            origin_latitude=34.0522,
            origin_longitude=-118.2437,
            destination_latitude=37.7749,
            destination_longitude=-122.4194,
            distance_km=616.803,
            charge_used_kwh=88.202829,
            percentage_charge_used=50.0,
            round_trip_charge_used_kwh=176.405658,
            round_trip_percentage_used=100.0,
            ev_type=self.ev_type
        )

        self.assertEqual(journey.driving_style, DrivingStyle.REGULAR.name)

    def test_charge_calculation_with_aggressive_driving_style(self):
        """Test charge calculation with aggressive driving style."""
        journey = Journey.objects.create(
            origin_latitude=34.0522,
            origin_longitude=-118.2437,
            destination_latitude=37.7749,
            destination_longitude=-122.4194,
            distance_km=616.803,
            charge_used_kwh=88.202829,
            percentage_charge_used=50.0,
            round_trip_charge_used_kwh=176.405658,
            round_trip_percentage_used=100.0,
            ev_type=self.ev_type,
            driving_style=DrivingStyle.AGGRESSIVE.name  # Setting aggressive driving style
        )

        expected_charge_used = journey.distance_km * \
            (self.ev_type.efficiency_kwh_per_km * DrivingStyle.AGGRESSIVE.value)
        percentage_charge_used = (
            expected_charge_used / self.ev_type.battery_capacity_kwh) * 100

        self.assertAlmostEqual(journey.charge_used_kwh,
                               expected_charge_used, places=2)
        self.assertAlmostEqual(
            journey.percentage_charge_used, percentage_charge_used, places=2)
