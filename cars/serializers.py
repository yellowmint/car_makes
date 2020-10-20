from rest_framework import serializers

from cars.models import Car


class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make_name', 'model_name']
