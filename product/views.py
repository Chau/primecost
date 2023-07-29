from django.shortcuts import render
from django.views.generic import ListView, CreateView

from .models import Dish, Ingredient
# from .forms import IngredientForm

# Create your views here.


class DishListView(ListView):
    model = Dish


class IngredientCreateView(CreateView):
    model = Ingredient
    fields = ('name', 'description', 'unit', 'price')
    # form_class = IngredientForm
