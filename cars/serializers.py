import requests
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from cars.models import Car, Rate

VEHICLE_API_URL = 'https://vpic.nhtsa.dot.gov'


class CarSerializer(serializers.ModelSerializer):
    average_rate = serializers.FloatField(read_only=True)
    rates_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'make_name', 'model_name', 'average_rate', 'rates_count']

        validators = [
            UniqueTogetherValidator(
                queryset=Car.objects.all(),
                fields=['make_name', 'model_name']
            )
        ]

    def validate(self, attrs):
        resp = requests.get(f'{VEHICLE_API_URL}/api/vehicles/getmodelsformake/{attrs["make_name"]}?format=json')
        cars = resp.json()['Results']

        attrs['make_name'] = attrs['make_name'].lower()
        attrs['model_name'] = attrs['model_name'].lower()

        for car in cars:
            if car['Make_Name'].lower() == attrs['make_name'] and car['Model_Name'].lower() == attrs['model_name']:
                return attrs

        raise serializers.ValidationError('given make and model not exist in reality and cannot be saved')


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['car', 'value']
