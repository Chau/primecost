from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.generic import ListView, CreateView, UpdateView, View

from .models import Dish, Ingredient
from .forms import DishForm, IngredientFormset

# Create your views here.

def ingredient_list_json(request):
    ingredients_json = Ingredient.search_ingredient()
    return JsonResponse(ingredients_json, safe=False)


class DishListView(ListView):
    model = Dish


def dish_create_view(request):
    if request.method == "POST":
        dish_form = DishForm(request.POST)
        ingredient_formset = IngredientFormset(request.POST)
        if ingredient_formset.is_valid():
            dish = dish_form.dish_save(ingredient_formset.cleaned_data)
            # TODO: change to dish with argument dish_id
            return redirect('dish_list')
        # TODO: add error output
        return render(request, template_name='product/dish_form.html')
    elif request.method == "GET":
        ingredient_formset = IngredientFormset()
        return render(request, template_name='product/dish_form.html',
                      context={'ingredient_formset': ingredient_formset})
    else:
        return HttpResponseNotAllowed(permitted_methods=('POST', 'GET'))

    return render(request, template_name='product/dish_form.html')


class DishCreateView(CreateView):
    success_url = '/dish/list'
    model = Dish
    # fields = ('name', 'description', 'ingredient')
    form_class = DishForm

    def dispatch(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
        return super(DishCreateView, self).dispatch(request, *args, **kwargs)


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
