from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from .models import Dish, Ingredient
# from .forms import IngredientForm

# Create your views here.


class DishListView(ListView):
    model = Dish


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
