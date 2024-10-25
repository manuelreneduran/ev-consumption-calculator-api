import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EVType, Journey, DrivingStyle
from .serializers import EVTypeSerializer, JourneySerializer
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured
import requests

# Load environment variables
load_dotenv()

# Get environment variables with validation


def get_env_variable(var_name):
    value = os.environ.get(var_name)
    if value is None:
        raise ImproperlyConfigured(
            f"{var_name} environment variable is not set")
    return value


google_maps_api_key = get_env_variable('GOOGLE_MAPS_API_KEY')


class EVTypeListView(APIView):
    def get(self, request):
        ev_types = EVType.objects.all()
        serializer = EVTypeSerializer(ev_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChargeEstimateView(APIView):
    def post(self, request):
        data = request.data
        origin_latitude = data.get('origin_latitude')
        origin_longitude = data.get('origin_longitude')
        destination_latitude = data.get('destination_latitude')
        destination_longitude = data.get('destination_longitude')
        driving_style = data.get('driving_style')
        ev_type_id = data.get('ev_type')

        # Retrieve EV type details
        try:
            ev_type = EVType.objects.get(id=ev_type_id)
        except EVType.DoesNotExist:
            return Response({"error": "EV type not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch route distance using a map API (e.g., Google Maps API)
        # Example placeholder for route distance (km)
        try:
            result = calculate_charge_usage(
                origin_latitude,
                origin_longitude,
                destination_latitude,
                destination_longitude,
                ev_type.battery_capacity_kwh,
                ev_type.efficiency_kwh_per_km,
                driving_style)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Save and return result
        journey = Journey.objects.create(
            origin_latitude=origin_latitude,
            origin_longitude=origin_longitude,
            destination_latitude=destination_latitude,
            destination_longitude=destination_longitude,
            ev_type=ev_type,
            distance_km=result['distance_km'],
            charge_used_kwh=result['charge_used_kwh'],
            percentage_charge_used=result['percentage_charge_used'],
            round_trip_charge_used_kwh=result['round_trip_charge_used_kwh'],
            round_trip_percentage_used=result['round_trip_percentage_used'],
            driving_style=driving_style
        )
        serializer = JourneySerializer(journey)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def calculate_charge_usage(origin_latitude, origin_longitude, destination_latitude, destination_longitude, battery_capacity_kwh, efficiency_kwh_per_km, driving_style):
    # Get the distance using the mapping API
    distance_km = get_route_distance(
        origin_latitude, origin_longitude, destination_latitude, destination_longitude)

    if distance_km is None:
        return {"error": "Could not calculate distance."}

    # Get the efficiency multiplier from the driving style
    efficiency_multiplier = DrivingStyle[driving_style].value

    # Calculate adjusted efficiency
    adjusted_efficiency = efficiency_kwh_per_km * efficiency_multiplier

    # Calculate charge used
    charge_used_kwh = distance_km * adjusted_efficiency

    # Calculate the percentage of charge used
    percentage_charge_used = (charge_used_kwh / battery_capacity_kwh) * 100

    # Calculate the round-trip charge usage and percentage
    round_trip_distance_km = distance_km * 2
    round_trip_charge_used_kwh = round_trip_distance_km * adjusted_efficiency
    round_trip_percentage_used = (
        round_trip_charge_used_kwh / battery_capacity_kwh) * 100

    # Create a response with all relevant data
    return {
        "distance_km": distance_km,
        "charge_used_kwh": charge_used_kwh,
        "percentage_charge_used": percentage_charge_used,
        "round_trip_charge_used_kwh": round_trip_charge_used_kwh,
        "round_trip_percentage_used": round_trip_percentage_used,
    }

# Helper function to calculate route distance (implement API call logic here)


def get_route_distance(origin_latitude, origin_longitude,  destination_latitude, destination_longitude):
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={origin_latitude},{
        origin_longitude}&destinations={destination_latitude},{destination_longitude}&key={google_maps_api_key}'

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data['status'] == 'OK':
        # Extracting the distance value from the response
        # Distance in meters
        distance = data['rows'][0]['elements'][0]['distance']['value']
        return distance / 1000  # Convert to kilometers
    else:
        print(f"Error: {data.get('error_message', 'Unknown error')}")
        return None  # Or handle the error as needed
