import pytest
import typing as t

from django.urls import reverse
from django.test import Client

from product.models import Ingredient, Dish, DishIngredient

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
class DishListTest:
    def test_empty_db(self, client: Client):
        response = client.get(reverse('dish_list'))
        assert response.status_code == 200

    def test_list_success(
            self, client: Client, dish_list: t.List[Dish]
    ):
        response = client.get(reverse('dish_list'))
        assert response.status_code == 200


# create
class DishCreateTest:

    def test_add_dish_to_empty_db(
            self, client: Client, ingredient_list: t.List[Ingredient]
    ):
        response = client.post(
            reverse('dish_create'),
            {
                'name': 'Торт Байкал',
                'description': 'Самый вкусный торт из Сибири',
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-1-ingredient_id': 1001,
                'form-1-ingredient_name': 'Яйцо',
                'form-1-ingredient_amount': 2,
                'form-1-ingredient_unit': 'шт',
                'form-2-ingredient_id': 1002,
                'form-2-ingredient_name': 'Мука',
                'form-2-ingredient_amount': 0.3,
                'form-2-ingredient_unit': 'кг',
                'form-3-ingredient_id': 1003,
                'form-3-ingredient_name': 'Сахар',
                'form-3-ingredient_amount': 0.2,
                'form-3-ingredient_unit': 'кг'
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        assert Ingredient.objects.count() == 3
        dish = Dish.objects.first()
        assert dish.name == 'Торт Байкал'
        assert dish.description == 'Самый вкусный торт из Сибири'
        assert dish.ingredient.count() == 3

    def test_add_dish_to_not_empty_db(
            self,
            client: Client,
            dish_w_ingredient: Dish,
            ingredient_list: t.List[Ingredient]
    ):
        response = client.post(
            reverse('dish_create'),
            {
                'name': 'Торт Байкал',
                'description': 'Самый вкусный торт из Сибири',
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-1-ingredient_id': 1001,
                'form-1-ingredient_name': 'Яйцо',
                'form-1-ingredient_amount': 2,
                'form-1-ingredient_unit': 'шт',
                'form-2-ingredient_id': 1002,
                'form-2-ingredient_name': 'Мука',
                'form-2-ingredient_amount': 0.3,
                'form-2-ingredient_unit': 'кг',
                'form-3-ingredient_id': 1003,
                'form-3-ingredient_name': 'Сахар',
                'form-3-ingredient_amount': 0.2,
                'form-3-ingredient_unit': 'кг'
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 2
        assert Ingredient.objects.count() == 4

        dish = Dish.objects.exclude(pk=dish_w_ingredient.pk).first()
        assert dish.name == 'Торт Байкал'
        assert dish.description == 'Самый вкусный торт из Сибири'
        assert dish.ingredient.count() == 3

    def test_add_to_dish_list(
            self,
            client: Client,
            dish_list: t.List[Dish],
            ingredient_list: t.List[Ingredient]
    ):
        response = client.post(
            reverse('dish_create'),
            {
                'name': 'Торт Байкал',
                'description': 'Самый вкусный торт из Сибири',
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-1-ingredient_id': 1001,
                'form-1-ingredient_name': 'Яйцо',
                'form-1-ingredient_amount': 2,
                'form-1-ingredient_unit': 'шт',
                'form-2-ingredient_id': 1002,
                'form-2-ingredient_name': 'Мука',
                'form-2-ingredient_amount': 0.3,
                'form-2-ingredient_unit': 'кг',
                'form-3-ingredient_id': 1003,
                'form-3-ingredient_name': 'Сахар',
                'form-3-ingredient_amount': 0.2,
                'form-3-ingredient_unit': 'кг'
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 4
        assert Ingredient.objects.count() == 5

        dish = Dish.objects.exclude(
            pk__in=[d.pk for d in dish_list]
        ).first()
        assert dish.name == 'Торт Байкал'
        assert dish.description == 'Самый вкусный торт из Сибири'
        assert dish.ingredient.count() == 3

    # TODO: remove skip mark after error handling
    @pytest.mark.skip
    def test_add_dish_w_very_long_name(
            self,
            client: Client,
            ingredient_list: t.List[Ingredient]
    ):
        response = client.post(
            reverse('dish_create'),
            {
                'name': 'ОченьОченьОченьОченьОченьОченьОченьОченьОченьОченьОченьОченьОченьОчень' \
                            'ОченьОченьОченьОченьОченьОченьОченьОченьОчень длинное название',
                'description': 'Самый вкусный торт из Сибири',
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-1-ingredient_id': 1001,
                'form-1-ingredient_name': 'Яйцо',
                'form-1-ingredient_amount': 2,
                'form-1-ingredient_unit': 'шт',
                'form-2-ingredient_id': 1002,
                'form-2-ingredient_name': 'Мука',
                'form-2-ingredient_amount': 0.3,
                'form-2-ingredient_unit': 'кг',
                'form-3-ingredient_id': 1003,
                'form-3-ingredient_name': 'Сахар',
                'form-3-ingredient_amount': 0.2,
                'form-3-ingredient_unit': 'кг'
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 0


# update
class DishUpdateTest:

    pass

# delete
class DishDeleteJsonTest:


    def test_delete_from_empty_db(self, client: Client):
        response = client.post(
            reverse('dish_delete_json', kwargs={'pk': 1000}),
            content_type="application/json")
        assert response.status_code == 200
        assert response.json() == {
            'status': 'error', 'message': 'Нет такого блюда.'
        }

    def test_delete_only_dish(
            self,
            client: Client,
            dish_w_ingredient: Dish
    ):
        response = client.post(
            reverse('dish_delete_json', kwargs={'pk': dish_w_ingredient.pk}),
            content_type="application/json")
        assert response.status_code == 200
        assert response.json() == {'status': 'ok'}
        assert Dish.objects.count() == 0
        assert Ingredient.objects.count() == 1
        assert DishIngredient.objects.count() == 0

    def test_delete_from_list(
            self,
            client: Client,
            dish_list: t.List[Dish]
    ):
        dish_id = dish_list[0].pk
        assert DishIngredient.objects.filter(dish__id=dish_id).count() == 1
        response = client.post(
            reverse('dish_delete_json', kwargs={'pk': dish_id}),
            content_type="application/json")
        assert response.status_code == 200
        assert response.json() == {'status': 'ok'}
        assert Dish.objects.count() == 2
        assert Ingredient.objects.count() == 5
        assert DishIngredient.objects.filter(dish__id=dish_id).count() == 0

    def test_wrong_pk_on_not_empty_db(
            self,
            client: Client,
            dish_list: t.List[Dish]
    ):
        response = client.post(
            reverse('dish_delete_json', kwargs={'pk': 10000}),
            content_type="application/json")
        assert response.status_code == 200
        assert response.json() == {
            'status': 'error', 'message': 'Нет такого блюда.'
        }
        assert Dish.objects.count() == 3
        assert Ingredient.objects.count() == 5
        assert DishIngredient.objects.count() == 5

