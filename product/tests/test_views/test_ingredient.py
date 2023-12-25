import pytest
import typing as t

from django.urls import reverse
from django.test import Client

from product.models import Ingredient

pytestmark = pytest.mark.django_db

@pytest.fixture
def client() -> Client:
    return Client()


# read detail
class IngredientReadTest:
    def test_empty_model_fail(self, client: Client):
        response = client.get(reverse('ingredient_detail', kwargs={'pk': 1}))
        assert response.status_code == 404

    def test_detail_not_empty_model_fail(
            self, client: Client, ingredient_w_descr: Ingredient
    ):
        response = client.get(reverse('ingredient_detail', kwargs={'pk': 2000}))
        assert response.status_code == 404

    def test_detail_wo_descr(
            self, client: Client, ingredient_wo_descr: Ingredient
    ):
        response = client.get(reverse('ingredient_detail', kwargs={'pk': 1}))
        assert response.status_code == 200

    def test_detail_w_descr(
            self, client: Client, ingredient_w_descr: Ingredient
    ):
        response = client.get(reverse('ingredient_detail', kwargs={'pk': 2}))
        assert response.status_code == 200


# read list of ingredients
class IngredientListTest:

    def test_empty_list(self, client: Client):
        response = client.get(reverse('ingredient_list'))
        assert response.status_code == 200

    def test_list(
            self, client: Client, ingredient_list: t.List[Ingredient]
    ):
        response = client.get(reverse('ingredient_list'))
        assert response.status_code == 200


# list_json
class IngredientListJsonTest:

    def test_empty_list(self, client: Client):
        response = client.get(reverse('ingredient_list_json'), content_type="application/json")
        assert response.status_code == 200
        assert response.json() == []

    def test_one_ingredient(
            self, client: Client, ingredient_w_descr: Ingredient
    ):
        response = client.get(reverse('ingredient_list_json'), content_type="application/json")
        assert response.status_code == 200
        assert response.json() == [
            {
                'name': 'Ингредиент 2',
                'id': ingredient_w_descr.id,
                'units': [{
                    'name': 'г',
                    'value': 'грамм',
                    'id': ingredient_w_descr.unit.id
                }]
            }
        ]

    def test_list_ingredient(
            self, client: Client, ingredient_list: t.List[Ingredient]
    ):
        response = client.get(reverse('ingredient_list_json'), content_type="application/json")
        assert response.status_code == 200
        assert response.json() == [
            {
                'name': 'Ингредиент для списка 1',
                'id': 1001,
                'units': [{
                    'name': 'г',
                    'value': 'грамм',
                    'id': 3
                }]
            },
            {
                'name': 'Ингредиент для списка 2',
                'id': 1002,
                'units': [{
                    'name': 'г',
                    'value': 'грамм',
                    'id': 3
                }]
            },
            {
                'name': 'Ингредиент для списка 3',
                'id': 1003,
                'units': [{
                    'name': 'г',
                    'value': 'грамм',
                    'id': 3
                }]
            }
        ]


# create
# update
# delete