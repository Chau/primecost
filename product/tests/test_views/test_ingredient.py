import pytest
import typing as t
import decimal

from django.urls import reverse
from django.test import Client

from product.models import Ingredient, Dish

pytestmark = pytest.mark.django_db


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
    # pytest.mark.usefixtures('client')

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
class IngredientCreateTest:

    def test_add_ingredient_wo_descr_to_empty_db(self, client: Client):
        response = client.post(
            reverse('ingredient_create'),
            {
                'pk': 1,
                'name': 'Создание ингредиента 1',
                'unit': 3,
                'price': 5
            }
        )
        assert response.status_code == 302
        assert Ingredient.objects.count() == 1
        ingredient = Ingredient.objects.get(pk=1)
        assert ingredient.name == 'Создание ингредиента 1'
        assert ingredient.description == ''
        assert ingredient.unit.pk == 3
        assert ingredient.price == 5

    def test_add_ingredient_w_descr_to_empty_db(self, client: Client):
        response = client.post(
            reverse('ingredient_create'),
            {
                'pk': 1,
                'name': 'Создание ингредиента 1',
                'description': 'Описание для ингредиента 1',
                'unit': 3,
                'price': 1
            }
        )
        assert response.status_code == 302
        assert Ingredient.objects.count() == 1
        ingredient = Ingredient.objects.get(pk=1)
        assert ingredient.name == 'Создание ингредиента 1'
        assert ingredient.description == 'Описание для ингредиента 1'
        assert ingredient.unit.pk == 3
        assert ingredient.price == 1

    def test_add_decimal_price(self, client: Client):
        response = client.post(
            reverse('ingredient_create'),
            {
                'pk': 1,
                'name': 'Создание ингредиента 1',
                'unit': 3,
                'price': 1.1
            }
        )
        assert response.status_code == 302
        assert Ingredient.objects.count() == 1
        ingredient = Ingredient.objects.get(pk=1)
        assert ingredient.name == 'Создание ингредиента 1'
        assert ingredient.description == ''
        assert ingredient.unit.pk == 3
        assert ingredient.price == decimal.Decimal('1.10')

    def test_add_to_not_empty_db(
            self, client: Client, ingredient_w_descr: Ingredient
    ):
        response = client.post(
            reverse('ingredient_create'),
            {
                'name': 'Создание ингредиента 1',
                'unit': 3,
                'price': 5
            }
        )
        assert response.status_code == 302
        assert Ingredient.objects.count() == 2
        ingredient = Ingredient.objects.get(name='Создание ингредиента 1')
        assert ingredient.name == 'Создание ингредиента 1'
        assert ingredient.description == ''
        assert ingredient.unit.pk == 3
        assert ingredient.price == 5

    def test_add_to_list_of_ingredients(
            self, client: Client, ingredient_list: t.List[Ingredient]
    ):
        response = client.post(
            reverse('ingredient_create'),
            {
                'name': 'Создание ингредиента 1',
                'unit': 3,
                'price': 0.1
            }
        )
        assert response.status_code == 302
        assert Ingredient.objects.count() == 4
        ingredient = Ingredient.objects.get(name='Создание ингредиента 1')
        assert ingredient.name == 'Создание ингредиента 1'
        assert ingredient.description == ''
        assert ingredient.unit.pk == 3
        assert ingredient.price == decimal.Decimal('0.10')

    def test_no_data(self, client: Client):
        response = client.post(reverse('ingredient_create'))
        assert response.status_code == 200
        assert Ingredient.objects.count() == 0

    def test_very_long_name(self, client: Client):
        response = client.post(
            reverse('ingredient_create'),
            {
                'pk': 1,
                'name': 'veryveryveryveryveryveryveryveryveryveryveryveryveryveryveryverylongname',
                'description': 'Описание для ингредиента 1',
                'unit': 3,
                'price': 1
            }
        )
        assert response.status_code == 200
        assert Ingredient.objects.count() == 0


# update
class IngredientUpdateTest:

    def test_empty_db(self, client: Client):
        response = client.post(
            reverse('ingredient_edit', kwargs={'pk': 1})
        )
        assert response.status_code == 404

    def test_wrong_id_on_not_empty_db(
            self, client: Client, ingredient_w_descr: Ingredient
    ):
        response = client.post(
            reverse('ingredient_edit', kwargs={'pk': 10000})
        )
        assert response.status_code == 404

    def test_no_data(
            self, client: Client, ingredient_w_descr: Ingredient
    ):
        response = client.post(
            reverse('ingredient_edit', kwargs={'pk': ingredient_w_descr.pk})
        )
        # not success
        assert response.status_code == 200

    def test_edit_ingredient(
            self, client: Client, ingredient_w_descr: Ingredient
    ):
        response = client.post(
            reverse('ingredient_edit', kwargs={'pk': ingredient_w_descr.pk}),
            {
                'name': 'Редактированный ингредиент',
                'description': 'Редактированное описание',
                'unit': 3,
                'price': 1
            }
        )
        # redirect if success
        assert response.status_code == 302
        assert Ingredient.objects.count() == 1
        ingredient = Ingredient.objects.get(pk=ingredient_w_descr.pk)
        assert ingredient.name == 'Редактированный ингредиент'
        assert ingredient.description == 'Редактированное описание'
        assert ingredient.unit.pk == 3
        assert ingredient.price == 1

    def test_edit_unit(
            self, client: Client, ingredient_w_descr: Ingredient
    ):
        response = client.post(
            reverse('ingredient_edit', kwargs={'pk': ingredient_w_descr.pk}),
            {
                'name': ingredient_w_descr.name,
                'description': ingredient_w_descr.description,
                'unit': 1,
                'price': ingredient_w_descr.price
            }
        )
        # redirect if success
        assert response.status_code == 302
        assert Ingredient.objects.count() == 1
        ingredient = Ingredient.objects.get(pk=ingredient_w_descr.pk)
        assert ingredient.name == 'Ингредиент 2'
        assert ingredient.description == 'Описание ингредиента 2'
        assert ingredient.unit.pk == 1
        assert ingredient.price == 0.5

    def test_one_ingredient_from_list(
            self, client: Client, ingredient_list: t.List[Ingredient]
    ):
        response = client.post(
            reverse('ingredient_edit', kwargs={'pk': 1002}),
            {
                'name': 'Редактированный ингредиент из списка',
                'description': 'Редактированное описание из списка',
                'unit': 1,
                'price': 10
            }
        )
        # redirect if success
        assert response.status_code == 302
        assert Ingredient.objects.count() == 3
        ingredient = Ingredient.objects.get(pk=1002)
        assert ingredient.name == 'Редактированный ингредиент из списка'
        assert ingredient.description == 'Редактированное описание из списка'
        assert ingredient.unit.pk == 1
        assert ingredient.price == 10

    def test_update_w_very_long_name(
            self, client: Client, ingredient_w_descr: Ingredient
    ):
        response = client.post(
            reverse('ingredient_edit', kwargs={'pk': ingredient_w_descr.pk}),
            {
                'name': 'veryveryveryveryveryveryveryveryveryveryveryveryveryveryveryverylongname',
                'description': 'Редактированное описание из списка',
                'unit': 1,
                'price': 10
            }
        )
        # not success
        assert response.status_code == 200
        assert Ingredient.objects.count() == 1
        ingredient = Ingredient.objects.get(pk=ingredient_w_descr.pk)
        assert ingredient.name == 'Ингредиент 2'
        assert ingredient.description == 'Описание ингредиента 2'
        assert ingredient.unit.pk == 3
        assert ingredient.price == 0.5


# delete_json
class IngredientDeleteJsonTest:

    def test_empty_db(self, client: Client):
        response = client.post(
            reverse('ingredient_delete_json', kwargs={'pk': 1000}),
            content_type="application/json")
        assert response.status_code == 200
        assert response.json() == {
            'status': 'error',
            'message': 'Ингредиент не существует в базе'
        }

    def test_wrong_pk_on_not_empty_db(
            self, client: Client, ingredient_w_descr: Ingredient
    ):
        response = client.post(
            reverse('ingredient_delete_json', kwargs={'pk': 1000}),
            content_type="application/json")
        assert Ingredient.objects.count() == 1
        assert response.status_code == 200
        assert response.json() == {
            'status': 'error',
            'message': 'Ингредиент не существует в базе'
        }

    def test_success(self, client: Client, ingredient_w_descr: Ingredient):
        response = client.post(
            reverse(
                'ingredient_delete_json',
                kwargs={'pk': ingredient_w_descr.pk}
            ),
            content_type="application/json"
        )
        assert response.status_code == 200
        assert response.json() == {'status': 'ok'}
        assert Ingredient.objects.count() == 0

    def test_success_deleting_from_ingredients_list(
            self, client: Client, ingredient_list: t.List[Ingredient]
    ):
        assert Ingredient.objects.count() == 3
        response = client.post(
            reverse(
                'ingredient_delete_json',
                kwargs={'pk': 1002}
            ),
            content_type="application/json"
        )
        assert response.status_code == 200
        assert response.json() == {'status': 'ok'}
        assert Ingredient.objects.count() == 2
        with pytest.raises(Ingredient.DoesNotExist):
            Ingredient.objects.get(pk=1002)

    def test_fail_cause_dish_exists(
            self,
            client: Client,
            ingredient_w_descr: Ingredient,
            dish_w_ingredient: Dish
    ):
        # There is dish exists
        response = client.post(
            reverse(
                'ingredient_delete_json',
                kwargs={'pk': ingredient_w_descr.pk}
            ),
            content_type="application/json"
        )
        assert response.status_code == 200
        assert response.json() == {
            'status': 'error',
            'message': 'Невозможно удалить ингредиент "{}", так как он является частью следующих блюд: \n{}'
                    .format(ingredient_w_descr.name, dish_w_ingredient.name)
        }
        assert Ingredient.objects.count() == 1

    def test_success_another_ingredient(
            self,
            client: Client,
            ingredient_wo_descr: Ingredient,
            dish_w_ingredient: Dish
    ):
        # Remove ingredient that is not of dish_w_ingredient
        assert Ingredient.objects.count() == 2
        response = client.post(
            reverse(
                'ingredient_delete_json',
                kwargs={'pk': ingredient_wo_descr.pk}
            ),
            content_type="application/json"
        )
        assert response.status_code == 200
        assert response.json() == {'status': 'ok'}
        assert Ingredient.objects.count() == 1
        with pytest.raises(Ingredient.DoesNotExist):
            Ingredient.objects.get(pk=ingredient_wo_descr.pk)


# delete
