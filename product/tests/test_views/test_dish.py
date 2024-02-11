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

    def test_add_dish_wo_ingredients(self, client: Client):
        response = client.post(
            reverse('dish_create'),
            {
                'name': 'Торт Байкал',
                'description': 'Самый вкусный торт из Сибири',
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.first()
        assert dish.name == 'Торт Байкал'
        assert dish.description == 'Самый вкусный торт из Сибири'
        assert dish.ingredient.count() == 0

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

    def test_update_empty_db(self, client: Client):
        response = client.post(
            reverse('dish_edit', kwargs={'pk': 10000}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': 'Блюдо дна',
                'description': 'Описание блюда дна',
                'form-TOTAL_FORMS': 2,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': 2,
                'form-0-ingredient_name': 'Яйцо',
                'form-0-ingredient_amount': 3,
                'form-0-ingredient_unit': 'шт',
                'form-1-ingredient_id': 6,
                'form-1-ingredient_name': 'Сахар',
                'form-1-ingredient_amount': 0.2,
                'form-1-ingredient_unit': 'кг'
            }
        )
        assert response.status_code == 404

    def test_404_on_not_empty_db(
            self,
            client: Client,
            dish_w_ingredient: Dish
    ):
        response = client.post(
            reverse('dish_edit', kwargs={'pk': 10000}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': 'Блюдо дна',
                'description': 'Описание блюда дна',
                'form-TOTAL_FORMS': 2,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': 2,
                'form-0-ingredient_name': 'Яйцо',
                'form-0-ingredient_amount': 3,
                'form-0-ingredient_unit': 'шт',
                'form-1-ingredient_id': 6,
                'form-1-ingredient_name': 'Сахар',
                'form-1-ingredient_amount': 0.2,
                'form-1-ingredient_unit': 'кг'
            }
        )
        assert response.status_code == 404

    # update data
    def test_update_dish_wo_ingredient(
            self,
            client: Client,
            dish_wo_ingredients: Dish
    ):
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_wo_ingredients.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'id': dish_wo_ingredients.pk,
                'name': 'Блюдо дна',
                'description': 'Описание блюда дна',
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_wo_ingredients.pk)
        assert dish.name == 'Блюдо дна'
        assert dish.description == 'Описание блюда дна'
        assert Ingredient.objects.count() == 0
        
    def test_update_only_dish_data(
            self,
            client: Client,
            dish_w_ingredient: Dish,
            ingredient_w_descr: Ingredient
    ):
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_w_ingredient.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': 'Блюдо дна',
                'description': 'Описание блюда дна',
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': ingredient_w_descr.pk,
                'form-0-ingredient_name': ingredient_w_descr.name,
                'form-0-ingredient_amount': 200,
                'form-0-ingredient_unit': ingredient_w_descr.unit.designation
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_w_ingredient.pk)
        assert dish.name == 'Блюдо дна'
        assert dish.description == 'Описание блюда дна'
        assert Ingredient.objects.count() == 1
        assert dish.dishingredient_set.count() == 1

    def test_update_only_ingredient_data(
            self,
            client: Client,
            dish_w_ingredient: Dish,
            ingredient_w_descr: Ingredient
    ):
        assert Dish.objects.count() == 1
        assert Ingredient.objects.count() == 1
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_w_ingredient.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': dish_w_ingredient.name,
                'description': dish_w_ingredient.description,
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': ingredient_w_descr.pk,
                'form-0-ingredient_name': ingredient_w_descr.name,
                'form-0-ingredient_amount': 100,
                'form-0-ingredient_unit': ingredient_w_descr.unit.designation
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_w_ingredient.pk)
        assert dish.name == dish_w_ingredient.name
        assert dish.description == dish_w_ingredient.description
        assert Ingredient.objects.count() == 1
        ingredient = Ingredient.objects.first()
        assert dish.dishingredient_set.count() == 1
        dish_ingredient = dish.dishingredient_set.first()
        assert dish_ingredient.amount == 100
        assert dish_ingredient.ingredient.pk == ingredient.pk

    def test_update_dish_and_ingredient_data(
            self,
            client: Client,
            dish_w_ingredient: Dish,
            ingredient_w_descr: Ingredient
    ):
        assert Dish.objects.count() == 1
        assert Ingredient.objects.count() == 1
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_w_ingredient.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': 'Блюдо дна',
                'description': 'Описание блюда дна',
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': ingredient_w_descr.pk,
                'form-0-ingredient_name': ingredient_w_descr.name,
                'form-0-ingredient_amount': 100,
                'form-0-ingredient_unit': ingredient_w_descr.unit.designation
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_w_ingredient.pk)
        assert dish.name == 'Блюдо дна'
        assert dish.description == 'Описание блюда дна'
        assert Ingredient.objects.count() == 1
        ingredient = Ingredient.objects.first()
        assert dish.dishingredient_set.count() == 1
        dish_ingredient = dish.dishingredient_set.first()
        assert dish_ingredient.amount == 100
        assert dish_ingredient.ingredient.pk == ingredient.pk

    # add ingredients
    def test_add_ingredient_to_dish_wo_ingredient(
            self,
            client: Client,
            dish_wo_ingredients: Dish,
            ingredient_w_descr: Ingredient
    ):
        assert Dish.objects.count() == 1
        assert Ingredient.objects.count() == 1
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_wo_ingredients.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': dish_wo_ingredients.name,
                'description': dish_wo_ingredients.description,
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': ingredient_w_descr.pk,
                'form-0-ingredient_name': ingredient_w_descr.name,
                'form-0-ingredient_amount': 100,
                'form-0-ingredient_unit': ingredient_w_descr.unit.designation
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_wo_ingredients.pk)
        assert dish.name == dish_wo_ingredients.name
        assert dish.description == dish_wo_ingredients.description
        assert Ingredient.objects.count() == 1
        ingredient = Ingredient.objects.first()
        assert dish.dishingredient_set.count() == 1
        dish_ingredient = dish.dishingredient_set.first()
        assert dish_ingredient.amount == 100
        assert dish_ingredient.ingredient.pk == ingredient.pk

    def test_add_ingredient_and_update_dish__wo_ingredient_data_(
            self,
            client: Client,
            dish_wo_ingredients: Dish,
            ingredient_w_descr: Ingredient
    ):
        assert Dish.objects.count() == 1
        assert Ingredient.objects.count() == 1
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_wo_ingredients.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': 'Блюдо дна',
                'description': 'Описание блюда дна',
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': ingredient_w_descr.pk,
                'form-0-ingredient_name': ingredient_w_descr.name,
                'form-0-ingredient_amount': 100,
                'form-0-ingredient_unit': ingredient_w_descr.unit.designation
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_wo_ingredients.pk)
        assert dish.name == 'Блюдо дна'
        assert dish.description == 'Описание блюда дна'
        assert Ingredient.objects.count() == 1
        ingredient = Ingredient.objects.first()
        assert dish.dishingredient_set.count() == 1
        dish_ingredient = dish.dishingredient_set.first()
        assert dish_ingredient.amount == 100
        assert dish_ingredient.ingredient.pk == ingredient.pk

    def test_add_ingredient_to_dish_w_ingredients(
            self,
            client: Client,
            dish_w_ingredient: Dish,
            ingredient_w_descr: Ingredient,
            ingredient_wo_descr: Ingredient
    ):
        assert Dish.objects.count() == 1
        assert Ingredient.objects.count() == 2
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_w_ingredient.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': 'Блюдо дна',
                'description': 'Описание блюда дна',
                'form-TOTAL_FORMS': 2,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': ingredient_w_descr.pk,
                'form-0-ingredient_name': ingredient_w_descr.name,
                'form-0-ingredient_amount': 100,
                'form-0-ingredient_unit': ingredient_w_descr.unit.designation,
                'form-1-ingredient_id': ingredient_wo_descr.pk,
                'form-1-ingredient_name': ingredient_wo_descr.name,
                'form-1-ingredient_amount': 98,
                'form-1-ingredient_unit': ingredient_wo_descr.unit.designation,
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_w_ingredient.pk)
        assert dish.name == 'Блюдо дна'
        assert dish.description == 'Описание блюда дна'
        assert Ingredient.objects.count() == 2
        assert dish.dishingredient_set.count() == 2
        dish_ingredient_1 = dish.dishingredient_set.get(ingredient=ingredient_w_descr)
        assert dish_ingredient_1.amount == 100
        dish_ingredient_2 = dish.dishingredient_set.get(ingredient=ingredient_wo_descr)
        assert dish_ingredient_2.amount == 98

    # remove ingredients
    def test_remove_only_ingredient(
            self,
            client: Client,
            dish_w_ingredient: Dish,
            ingredient_w_descr: Ingredient
    ):
        assert Dish.objects.count() == 1
        assert Ingredient.objects.count() == 1
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_w_ingredient.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': dish_w_ingredient.name,
                'description': dish_w_ingredient.description,
                'form-TOTAL_FORMS': 0,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_w_ingredient.pk)
        assert dish.name == dish_w_ingredient.name
        assert dish.description == dish_w_ingredient.description
        assert Ingredient.objects.count() == 1
        assert dish.dishingredient_set.count() == 0

    def test_remove_from_ingredient_list(
            self,
            client: Client,
            dish_w_ingredient_list: Dish,
            ingredient_w_descr: Ingredient,
            ingredient_wo_descr: Ingredient
    ):
        assert Dish.objects.count() == 1
        assert Ingredient.objects.count() == 2
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_w_ingredient_list.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': dish_w_ingredient_list.name,
                'description': dish_w_ingredient_list.description,
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': ingredient_w_descr.pk,
                'form-0-ingredient_name': ingredient_w_descr.name,
                'form-0-ingredient_amount': 200,
                'form-0-ingredient_unit': ingredient_w_descr.unit.designation
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_w_ingredient_list.pk)
        assert dish.name == dish_w_ingredient_list.name
        assert dish.description == dish_w_ingredient_list.description
        assert Ingredient.objects.count() == 2
        assert dish.dishingredient_set.count() == 1
        dish_ingredient = dish.dishingredient_set.first()
        assert dish_ingredient.ingredient == ingredient_w_descr
        assert dish_ingredient.amount == 200

    # remove and add ingredients
    def test_remove_only_add_new_ingredient(
            self,
            client: Client,
            dish_w_ingredient: Dish,
            ingredient_w_descr: Ingredient,
            ingredient_wo_descr: Ingredient
    ):
        assert Dish.objects.count() == 1
        assert Ingredient.objects.count() == 2
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_w_ingredient.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': dish_w_ingredient.name,
                'description': dish_w_ingredient.description,
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': ingredient_wo_descr.pk,
                'form-0-ingredient_name': ingredient_wo_descr.name,
                'form-0-ingredient_amount': 150,
                'form-0-ingredient_unit': ingredient_wo_descr.unit.designation
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_w_ingredient.pk)
        assert dish.name == dish_w_ingredient.name
        assert dish.description == dish_w_ingredient.description
        assert Ingredient.objects.count() == 2
        assert dish.dishingredient_set.count() == 1
        dishingredient = dish.dishingredient_set.first()
        assert dishingredient.ingredient == ingredient_wo_descr
        assert dishingredient.amount == 150

    def test_remove_from_list_add_ingredient(
            self,
            client: Client,
            dish_w_ingredient_list: t.List[Dish],
            ingredient_w_descr: Ingredient,
            ingredient_wo_descr: Ingredient,
            ingredient_list: t.List[Ingredient]
    ):
        assert Dish.objects.count() == 1
        assert Ingredient.objects.count() == 5
        # remove ingredient_wo_descr
        # add ingredient_list - 3 шт
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_w_ingredient_list.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': dish_w_ingredient_list.name,
                'description': dish_w_ingredient_list.description,
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': ingredient_w_descr.pk,
                'form-0-ingredient_name': ingredient_w_descr.name,
                'form-0-ingredient_amount': 200,
                'form-0-ingredient_unit': ingredient_w_descr.unit.designation,
                'form-1-ingredient_id': ingredient_list[0].pk,
                'form-1-ingredient_name': ingredient_list[0].name,
                'form-1-ingredient_amount': 150,
                'form-1-ingredient_unit': ingredient_list[0].unit.designation,
                'form-2-ingredient_id': ingredient_list[1].pk,
                'form-2-ingredient_name': ingredient_list[1].name,
                'form-2-ingredient_amount': 100,
                'form-2-ingredient_unit': ingredient_list[1].unit.designation,
                'form-3-ingredient_id': ingredient_list[2].pk,
                'form-3-ingredient_name': ingredient_list[2].name,
                'form-3-ingredient_amount': 55,
                'form-3-ingredient_unit': ingredient_list[2].unit.designation,
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_w_ingredient_list.pk)
        assert dish.name == dish_w_ingredient_list.name
        assert dish.description == dish_w_ingredient_list.description
        assert Ingredient.objects.count() == 5
        assert dish.dishingredient_set.count() == 4
        assert dish.dishingredient_set.filter(ingredient=ingredient_wo_descr).count() == 0

    # remove and edit ingredients
    def test_remove_one_edit_remaining_ingredient(
            self,
            client: Client,
            dish_w_ingredient_list: Dish,
            ingredient_w_descr: Ingredient,
            ingredient_wo_descr: Ingredient
    ):
            assert Dish.objects.count() == 1
            assert Ingredient.objects.count() == 2
            response = client.post(
                reverse('dish_edit', kwargs={'pk': dish_w_ingredient_list.pk}),
                data={
                    'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                    'name': dish_w_ingredient_list.name,
                    'description': dish_w_ingredient_list.description,
                    'form-TOTAL_FORMS': 1,
                    'form-INITIAL_FORMS': 0,
                    'form-MIN_NUM_FORMS': 0,
                    'form-MAX_NUM_FORMS': 1000,
                    'form-0-ingredient_id': ingredient_w_descr.pk,
                    'form-0-ingredient_name': ingredient_w_descr.name,
                    'form-0-ingredient_amount': 98,
                    'form-0-ingredient_unit': ingredient_w_descr.unit.designation
                }
            )
            assert response.status_code == 302
            assert Dish.objects.count() == 1
            dish = Dish.objects.get(pk=dish_w_ingredient_list.pk)
            assert dish.name == dish_w_ingredient_list.name
            assert dish.description == dish_w_ingredient_list.description
            assert Ingredient.objects.count() == 2
            assert dish.dishingredient_set.count() == 1
            dish_ingredient = dish.dishingredient_set.first()
            assert dish_ingredient.ingredient == ingredient_w_descr
            assert dish_ingredient.amount == 98

    def test_remove_edit_and_add_ingredients(
            self,
            client: Client,
            dish_w_ingredient_list: t.List[Dish],
            ingredient_w_descr: Ingredient,
            ingredient_wo_descr: Ingredient,
            ingredient_list: t.List[Ingredient]
    ):
        assert Dish.objects.count() == 1
        assert Ingredient.objects.count() == 5
        # remove ingredient_wo_descr
        # add ingredient_list - 3 шт
        response = client.post(
            reverse('dish_edit', kwargs={'pk': dish_w_ingredient_list.pk}),
            data={
                'csrfmiddlewaretoken': 'ZPNxsqWNh1Zt73WZJXICSHX7OOFGN5chiZDvzzRNLUaH2HLf1O61Wc5FrvniopI3',
                'name': dish_w_ingredient_list.name,
                'description': dish_w_ingredient_list.description,
                'form-TOTAL_FORMS': 4,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,
                'form-0-ingredient_id': ingredient_w_descr.pk,
                'form-0-ingredient_name': ingredient_w_descr.name,
                'form-0-ingredient_amount': 98,
                'form-0-ingredient_unit': ingredient_w_descr.unit.designation,
                'form-1-ingredient_id': ingredient_list[0].pk,
                'form-1-ingredient_name': ingredient_list[0].name,
                'form-1-ingredient_amount': 150,
                'form-1-ingredient_unit': ingredient_list[0].unit.designation,
                'form-2-ingredient_id': ingredient_list[1].pk,
                'form-2-ingredient_name': ingredient_list[1].name,
                'form-2-ingredient_amount': 100,
                'form-2-ingredient_unit': ingredient_list[1].unit.designation,
                'form-3-ingredient_id': ingredient_list[2].pk,
                'form-3-ingredient_name': ingredient_list[2].name,
                'form-3-ingredient_amount': 55,
                'form-3-ingredient_unit': ingredient_list[2].unit.designation,
            }
        )
        assert response.status_code == 302
        assert Dish.objects.count() == 1
        dish = Dish.objects.get(pk=dish_w_ingredient_list.pk)
        assert dish.name == dish_w_ingredient_list.name
        assert dish.description == dish_w_ingredient_list.description
        assert Ingredient.objects.count() == 5
        assert dish.dishingredient_set.count() == 4
        assert dish.dishingredient_set.filter(ingredient=ingredient_wo_descr).count() == 0
        dishingredient = dish.dishingredient_set.get(ingredient=ingredient_w_descr)
        assert dishingredient.amount == 98

    # TODO: ingredients reordering


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

