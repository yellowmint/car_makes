import requests
from rest_framework import serializers

from cars.models import Car

VEHICLE_API_URL = 'https://vpic.nhtsa.dot.gov'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make_name', 'model_name']

    def validate(self, attrs):
        resp = requests.get(f'{VEHICLE_API_URL}/api/vehicles/getmodelsformake/{attrs["make_name"]}?format=json')
        cars = resp.json()['Results']

        attrs['make_name'] = attrs['make_name'].lower()
        attrs['model_name'] = attrs['model_name'].lower()

        for car in cars:
            if car['Make_Name'].lower() == attrs['make_name'] and car['Model_Name'].lower() == attrs['model_name']:
                return attrs

        raise serializers.ValidationError('given make and model not exist in reality and cannot be saved')
