from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, TemplateView

from ..forms import IngredientFormset, DishForm
from ..models import Dish


class DishDetailView(DetailView):
    model = Dish


class DishListView(ListView):
    model = Dish


class DishCreateView(TemplateView):
    template_name = 'dish_form_create.html'

    def get(self, request, *args, **kwargs):
        ingredient_formset = IngredientFormset()
        return render(request, template_name='product/dish_form_create.html',
                      context={'ingredient_formset': ingredient_formset})

    def post(self, request, *args, **kwargs):
        dish_form = DishForm(request.POST)
        ingredient_formset = IngredientFormset(request.POST)
        if ingredient_formset.is_valid():
            dish = dish_form.dish_save(ingredient_formset.cleaned_data)
        # TODO: change to dish with argument dish_id
        # TODO: show errors if not valid
        return redirect(dish)


class DishUpdateView(TemplateView):
    template_name = 'dish_form_update.html'

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
