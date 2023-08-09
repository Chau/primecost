from django.db import models

from glossary.models import MeasurementUnit


class Ingredient(models.Model):
    name = models.CharField(max_length=64, verbose_name='Наименование')
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.PROTECT, verbose_name='Единица измерения')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена в рублях за единицу')


class Dish(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    ingredient = models.ManyToManyField(Ingredient, through='DishIngredient')


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
