from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cars import views

router = DefaultRouter()
router.register(r'cars', views.CarViewSet)
router.register(r'rate', views.RateViewSet)
router.register(r'popular', views.PopularViewSet, basename='popular')

urlpatterns = [
    path('', include(router.urls)),
]
