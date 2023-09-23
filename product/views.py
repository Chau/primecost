from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, View

from .models import Dish, Ingredient
# from .forms import IngredientForm

# Create your views here.


class DishListView(ListView):
    model = Dish


class DishCreateView(CreateView):
    success_url = '/dish/list'
    model = Dish
    fields = ('name', 'description', 'ingredient')


class IngredientListJsonView(View):
    def dispatch(self, request, *args, **kwargs):
        ingredients_json = [
            {
              'name': 'яйцо',
              'id': '1',
              'units': [{'name': 'шт', 'value': 'piece', 'id': 1}]
            },
            {
              'name': 'мука',
              'id': 2,
              'units': [
                                {'name': 'грамм', 'value': 'g', 'id': 2},
                                {'name': 'килограмм', 'value': 'kg', 'id': 3}
                              ]
            },
            {
              'name': 'сахар',
              'id': 3,
              'units': [
                                {'name': 'грамм', 'value': 'g', 'id': 2},
                                {'name': 'килограмм', 'value': 'kg', 'id': 3}
                              ]
            }
          ]
        return JsonResponse(ingredients_json, safe=False)



class IngredientCreateView(CreateView):
    success_url = '/ingredient/create'
    model = Ingredient
    fields = ('name', 'description', 'unit', 'price')
    # form_class = IngredientForm


class IngredientUpdateView(UpdateView):

    model = Ingredient
    fields = ('name', 'description', 'unit', 'price')

    def get_success_url(self):
        return '/ingredient/{}/update'.format(self.object.id)
