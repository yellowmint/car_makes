from django.db import models


class Car(models.Model):
    make_name = models.CharField(max_length=250)
    model_name = models.CharField(max_length=250)
