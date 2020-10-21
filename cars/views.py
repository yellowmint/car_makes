from django.db.models import Avg, F, Count
from rest_framework import viewsets, mixins

from cars.models import Car, Rate
from cars.serializers import CarSerializer, RateSerializer
from cars.sql import Round


class CarViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_queryset(self):
        return super().get_queryset() \
            .annotate(average_rate=Round(Avg('rate__value'), 2)) \
            .annotate(rates_count=Count('rate')) \
            .order_by(F('average_rate').desc(nulls_last=True))


class PopularViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Car.objects.all() \
        .annotate(average_rate=Round(Avg('rate__value'), 2)) \
        .annotate(rates_count=Count('rate')) \
        .order_by(F('rates_count').desc(nulls_last=True))[:3]
    serializer_class = CarSerializer


class RateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
