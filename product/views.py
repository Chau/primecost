
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView

from .models import Dish, Ingredient
from .forms import DishForm, IngredientFormset

# Create your views here.


def ingredient_list_json(request):
    ingredients_json = Ingredient.search_ingredient()
    return JsonResponse(ingredients_json, safe=False)


class DishDetailView(DetailView):
    model = Dish


class DishListView(ListView):
    model = Dish


class DishCreateView(TemplateView):

    def get(self, request, *args, **kwargs):
        ingredient_formset = IngredientFormset()
        return render(request, template_name='product/dish_form.html',
                      context={'ingredient_formset': ingredient_formset})

    def post(self, request, *args, **kwargs):
        dish_form = DishForm(request.POST)
        ingredient_formset = IngredientFormset(request.POST)
        if ingredient_formset.is_valid():
            dish = dish_form.dish_save(ingredient_formset.cleaned_data)
        # TODO: change to dish with argument dish_id
        # TODO: show errors if not valid
        return redirect(dish)


class IngredientListView(ListView):
    model = Ingredient
    context_object_name = 'ingredients'

    def get_queryset(self):
        return Ingredient.objects.select_related().all()


class IngredientDetailView(DetailView):
    model = Ingredient


class IngredientCreateView(CreateView):
    success_url = '/ingredient/create'
    model = Ingredient
    fields = ('name', 'description', 'unit', 'price')
   

class IngredientUpdateView(UpdateView):
    model = Ingredient
    fields = ('name', 'description', 'unit', 'price')

    def get_success_url(self):
        return '/ingredient/{}/update'.format(self.object.id)
