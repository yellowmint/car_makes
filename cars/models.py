from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Car(models.Model):
    make_name = models.CharField(max_length=250)
    model_name = models.CharField(max_length=250)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['make_name', 'model_name'], name='unique_make_model')
        ]

    def __str__(self):
        return f'{self.make_name} {self.model_name}'


class Rate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
