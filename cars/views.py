from django.db.models import Avg, F
from rest_framework import viewsets, mixins

from cars.models import Car
from cars.serializers import CarSerializer, RateSerializer
from cars.sql import Round


class CarViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_queryset(self):
        return super().get_queryset() \
            .annotate(average_rate=Round(Avg('rate__value'), 2)) \
            .order_by(F('average_rate').desc(nulls_last=True))


class RateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RateSerializer
