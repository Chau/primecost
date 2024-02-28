import pytest
import typing as t

from django.test import Client

from glossary.models import MeasurementUnit
from product.models import Ingredient, Dish, DishIngredient

@pytest.fixture
def client() -> Client:
    return Client()


#ingredients
@pytest.fixture
def gramm_unit():
    return MeasurementUnit.objects.get(
        full_name='грамм'
    )


@pytest.fixture
def ingredient_wo_descr(gramm_unit: MeasurementUnit) -> Ingredient:
    return Ingredient.objects.create(
        pk=1,
        name='Ингредиент 1',
        unit=gramm_unit,
        price=0.5
    )


@pytest.fixture
def ingredient_w_descr(gramm_unit: MeasurementUnit) -> Ingredient:
    return Ingredient.objects.create(
        pk=2,
        name='Ингредиент 2',
        unit=gramm_unit,
        description='Описание ингредиента 2',
        price=0.5
    )


@pytest.fixture
def ingredient_list(gramm_unit: MeasurementUnit) -> t.List[Ingredient]:
    return Ingredient.objects.bulk_create(
        [
            Ingredient(
                pk=1001,
                name='Ингредиент для списка 1',
                unit=gramm_unit,
                description='Описание для ингредиента 1',
                price=1
            ),
            Ingredient(
                pk=1002,
                name='Ингредиент для списка 2',
                unit=gramm_unit,
                description='Описание для ингредиента 2',
                price=2
            ),
            Ingredient(
                pk=1003,
                name='Ингредиент для списка 3',
                unit=gramm_unit,
                description='Описание для ингредиента 3',
                price=3
            ),
        ]
    )


@pytest.fixture
def many_ingredients_list(gramm_unit: MeasurementUnit) -> t.List[Ingredient]:
    return Ingredient.objects.bulk_create(
        [
            Ingredient(
                pk=2001,
                name='Молоко',
                unit=gramm_unit,
                description='Описание для Молока',
                price=0.06
            ),
            Ingredient(
                pk=2002,
                name='Сахар',
                unit=gramm_unit,
                description='Описание для Сахара',
                price=0.058
            ),
            Ingredient(
                pk=2003,
                name='Манная крупа',
                unit=gramm_unit,
                description='Описание для Манной крупы',
                price=0.05
            ),
            Ingredient(
                pk=2004,
                name='Корица',
                unit=gramm_unit,
                description='Описание для Корицы',
                price=3
            ),
        ]
    )

# dishes
@pytest.fixture
def dish_wo_ingredients() -> Dish:
    return Dish.objects.create(
        name='Блюдо без ингридиентов',
        description='Описание для блюда без ингридиентов'
    )


@pytest.fixture
def dish_w_ingredient(ingredient_w_descr: Ingredient) -> Dish:
    dish = Dish.objects.create(
        name='Блюдо 1',
        description='Описание для блюда 1'
    )
    DishIngredient.objects.create(
        dish=dish,
        ingredient=ingredient_w_descr,
        amount=200
    )
    return dish

@pytest.fixture
def dish_w_ingredient_list(
        ingredient_w_descr: Ingredient,
        ingredient_wo_descr: Ingredient
) -> Dish:
    dish = Dish.objects.create(
        name='Блюдо 1',
        description='Описание для блюда 1'
    )
    DishIngredient.objects.create(
        dish=dish,
        ingredient=ingredient_w_descr,
        amount=200
    )
    DishIngredient.objects.create(
        dish=dish,
        ingredient=ingredient_wo_descr,
        amount=50
    )
    return dish


@pytest.fixture
def dish_list(
        ingredient_w_descr: Ingredient,
        ingredient_wo_descr: Ingredient,
        ingredient_list: t.List[Ingredient]
) -> t.List[Dish]:
    dish_list = []
    dish_list.append(Dish.objects.create(
        name='Блюдо для списка 1',
        description='Описание для блюда списка 1'
    ))
    DishIngredient.objects.create(
        dish=dish_list[0],
        ingredient=ingredient_w_descr,
        amount=200
    )
    dish_list.append(
        Dish.objects.create(
            name='Блюдо для списка 2',
            description='Описание для блюда списка 3'
        )
    )
    DishIngredient.objects.create(
        dish=dish_list[1],
        ingredient=ingredient_w_descr,
        amount=300
    )
    dish_list.append(
        Dish.objects.create(
            name='Блюдо для списка 3',
            description='Описание для блюда списка 3'
        )
    )
    for i, ingredient in enumerate(ingredient_list):
        DishIngredient.objects.create(
            dish=dish_list[2],
            ingredient=ingredient_w_descr,
            amount=150 + i
        )
    return dish_list

