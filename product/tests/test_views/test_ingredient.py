import pytest

from django.urls import reverse
from django.test import Client

from product.models import Ingredient

@pytest.fixture
def client():
    return Client()


# read detail
@pytest.mark.django_db
class TestDishRead:
    def test_empty_model_fail(self, client):
        response = client.get(reverse('ingredient_detail', kwargs={'pk': 1}))
        assert response.status_code == 404

    def test_detail_not_empty_model_fail(self, client, ingredient_w_descr):
        response = client.get(reverse('ingredient_detail', kwargs={'pk': 2000}))
        assert response.status_code == 404

    def test_detail_wo_descr(self, client, ingredient_wo_descr):
        response = client.get(reverse('ingredient_detail', kwargs={'pk': 1}))
        assert response.status_code == 200

    def test_detail_w_descr(self, client, ingredient_w_descr):
        response = client.get(reverse('ingredient_detail', kwargs={'pk': 2}))
        assert response.status_code == 200




# create
# update
# delete