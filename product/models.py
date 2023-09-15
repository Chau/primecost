from django.db import models

from glossary.models import MeasurementUnit


class Ingredient(models.Model):
    name = models.CharField(max_length=64, verbose_name='Наименование')
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.PROTECT, verbose_name='Единица измерения')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена в рублях за единицу')

    def __str__(self):
        return '{}, {}, {}'.format(self.name, self.unit, str(self.price))


class Dish(models.Model):
    name = models.CharField(max_length=128, verbose_name='Наименование блюда')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    ingredient = models.ManyToManyField(Ingredient, through='DishIngredient', verbose_name='Ингридиенты')


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
