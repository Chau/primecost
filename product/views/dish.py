from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, TemplateView

from ..forms import IngredientFormset, DishForm
from ..models import Dish


class DishDetailView(DetailView):
    model = Dish


class DishListView(ListView):
    model = Dish


class DishCreateView(TemplateView):
    template_name = 'product/dish_form_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredient_formset'] = IngredientFormset()

    # def get(self, request, *args, **kwargs):
    #     ingredient_formset = IngredientFormset()
    #     return render(request, template_name='product/dish_form_create.html',
    #                   context={'ingredient_formset': ingredient_formset})

    def post(self, request, *args, **kwargs):
        dish_form = DishForm(request.POST)
        ingredient_formset = IngredientFormset(request.POST)
        if ingredient_formset.is_valid():
            dish = dish_form.dish_save(ingredient_formset.cleaned_data)
        # TODO: change to dish with argument dish_id
        # TODO: show errors if not valid
        return redirect(dish)


class DishUpdateView(TemplateView):
    template_name = 'product/dish_form_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dish_id = context['pk']
        dish = Dish.objects.get(pk=dish_id)
        context['dish'] = dish
        # fill formset: {'ingredient_id': 1, 'ingredient_name': 'name', 'ingredient_amount': 2, 'ingredient_unit': 'шт'}
        ingredient_data = [
            {
                'ingredient_id': 0,
                'ingredient_name': '',
                'ingredient_amount': '',
                'ingredient_unit': ''
            }
        ]
        for dish_ingredient in dish.dishingredient_set.all():
            ingredient_data.append(
                    {
                        'ingredient_id': dish_ingredient.ingredient.id,
                        'ingredient_name': dish_ingredient.ingredient.name,
                        'ingredient_amount': dish_ingredient.amount,
                        'ingredient_unit': dish_ingredient.ingredient.unit.full_name
                    }

            )
        context['ingredient_formset'] = IngredientFormset(initial=ingredient_data)
        context['ingredient_len'] = len(ingredient_data) - 1
        return context

    # def get(self, request, *args, **kwargs):
    #     pass
    #
    def post(self, request, *args, **kwargs):
        dish_form = DishForm(request.POST)
        ingredient_formset = IngredientFormset(request.POST)
        if ingredient_formset.is_valid():
            dish = dish_form.dish_save(ingredient_formset.cleaned_data)
        # TODO: change to dish with argument dish_id
        # TODO: show errors if not valid
        return redirect(dish)
