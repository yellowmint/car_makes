from rest_framework import serializers

from cars.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make_name', 'model_name']

    def validate(self, attributes):
        if attributes['make_name'] == attributes['model_name']:
            raise serializers.ValidationError('make and model names cannot be equal')
