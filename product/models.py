import typing as t

from django.db import models
from django.utils.functional import cached_property

from glossary.models import MeasurementUnit


class Ingredient(models.Model):
    name = models.CharField(max_length=64, verbose_name='Наименование')
    unit = models.ForeignKey(MeasurementUnit, on_delete=models.PROTECT, verbose_name='Единица измерения')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Цена в рублях за единицу')

    def search_dishes(self):
        return [dishingredient.dish for dishingredient in self.dishingredient_set.all()]

    @classmethod
    def search_ingredient(cls) -> t.List:
        """
        TODO: add searching string
        Return list of ingredients with units
        :return: List
        """
        return [{
                    'name': ingredient.name,
                    'id': ingredient.id,
                    'units': [{
                        'name': ingredient.unit.designation,
                        'value': ingredient.unit.full_name,
                        'id': ingredient.unit.id
                    }]
                 } for ingredient in cls.objects.all()]

    def __str__(self) -> str:
        return '{}, {}, {}'.format(self.name, self.unit, str(self.price))


class Dish(models.Model):
    name = models.CharField(max_length=128, verbose_name='Наименование блюда')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    # TODO: rename to 'ingredients'
    ingredient = models.ManyToManyField(Ingredient, through='DishIngredient', verbose_name='Ингредиенты')

    @classmethod
    def delete_dish(cls, dish_id: int):
        # remove ingredients relation
        DishIngredient.objects.filter(dish__pk=dish_id).delete()
        # remove dish
        Dish.objects.filter(pk=dish_id).delete()
        return

    def get_absolute_url(self):
        return '/dish/{}'.format(self.pk)

    def save_ingredients(self, ingredients_data: t.List[t.Dict]) -> None:
        """
        Save ingredients of dish to DishIngredient model.
        Example of ingredients_data:
        [
            {},
            {
                'ingredient_id': 1,
                'ingredient_name': 'Яйцо белореченское, 1 кат.',
                'ingredient_amount': 2.0,
                'ingredient_unit': 'шт'
            },
            {
                'ingredient_id': 3,
                'ingredient_name': 'Молоко',
                'ingredient_amount': 0.2,
                'ingredient_unit': 'л'
            }
        ]
        :return:
        """

        for ingredient_item in ingredients_data:
            # TODO: add exception
            if not ingredient_item:
                continue
            ingredient = Ingredient.objects.get(pk=ingredient_item['ingredient_id'])
            DishIngredient.objects.update_or_create(
                dish=self, ingredient=ingredient, defaults={'amount': ingredient_item['ingredient_amount']}
            )
    #         TODO: add delete functional

    @cached_property
    def total(self) -> float:
        """
        Count total cost of dish
        :return:
        """
        total_sum = 0
        for dish_ingredient in self.dishingredient_set.all():
            total_sum += dish_ingredient.amount * float(dish_ingredient.ingredient.price)
        return total_sum


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    amount = models.FloatField()
