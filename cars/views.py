from rest_framework import viewsets, mixins

from cars.models import Car
from cars.serializers import CarSerializer, RateSerializer


class CarViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class RateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RateSerializer
