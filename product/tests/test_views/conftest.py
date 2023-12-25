import pytest
import typing as t

from glossary.models import MeasurementUnit
from product.models import Ingredient


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
