import pytest
import typing as t

from django.urls import reverse
from django.test import Client

from product.models import Ingredient

pytestmark = pytest.mark.django_db

@pytest.fixture
def client():
    return Client()


# read detail
class DishReadTest:
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
class DishListTest:

    def test_empty_list(self, client: Client):
        response = client.get(reverse('ingredient_list'))
        assert response.status_code == 200

    def test_list(
            self, client: Client, ingredient_list: t.List[Ingredient]
    ):
        response = client.get(reverse('ingredient_list'))
        assert response.status_code == 200

# create
# update
# delete