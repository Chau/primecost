import pytest
import typing as t

from django.urls import reverse
from django.test import Client

from product.models import Ingredient, Dish

pytestmark = pytest.mark.django_db


# read detail
class DishReadDetailTest:

    def test_empty_db(self, client: Client):
        response = client.get(reverse('dish_detail', kwargs={'pk': 1}))
        assert response.status_code == 404

    def test_wrong_pk(self, client: Client, dish_w_ingredient: Dish):
        response = client.get(reverse('dish_detail', kwargs={'pk': 100}))
        assert response.status_code == 404

    def test_success(self, client: Client, dish_w_ingredient: Dish):
        response = client.get(
            reverse('dish_detail', kwargs={'pk': dish_w_ingredient.pk})
        )
        assert response.status_code == 200

# list
# create
# update
# delete

