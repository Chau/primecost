from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView, UpdateView

from ..forms import IngredientFormset, DishForm
from ..models import Dish


def dish_delete_json(request, pk: int, *args, **kwargs):
    try:
        Dish.objects.get(pk=pk)
    except Dish.DoesNotExist:
        result = {'status': 'error', 'message': 'Нет такого блюда.'}
        return JsonResponse(result, safe=False)
    Dish.delete_dish(dish_id=pk)
    return JsonResponse({'status': 'ok'}, safe=False)


class DishDetailView(DetailView):
    model = Dish


class DishListView(ListView):
    model = Dish

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dishes'] = Dish.objects.all().order_by('-pk')
        return context


class DishCreateView(TemplateView):
    # TODO: Попробовать переделать на наследование от FormView
    template_name = 'product/dish_form_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredient_formset'] = IngredientFormset()
        return context

    def post(self, request, *args, **kwargs):
        dish_form = DishForm(request.POST)
        ingredient_formset = IngredientFormset(request.POST)
        if dish_form.is_valid():
            dish = dish_form.save()
        # TODO: handle exceptions: show errors if not valid
        if ingredient_formset.is_valid():
            dish.save_ingredients(ingredient_formset.cleaned_data)
        # if ingredient_formset.is_valid():
        #     dish = dish_form.dish_save(ingredient_formset.cleaned_data)
        # TODO: change to dish with argument dish_id
        # TODO: show errors if not valid
        return redirect(dish)


class DishUpdateView(UpdateView):
    template_name = 'product/dish_form_update.html'
    form_class = DishForm
    model = Dish

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        ingredient_data = []
        for dish_ingredient in context['dish'].dishingredient_set.all():
            ingredient_data.append(
                    {
                        'ingredient_id': dish_ingredient.ingredient.id,
                        'ingredient_name': dish_ingredient.ingredient.name,
                        'ingredient_amount': dish_ingredient.amount,
                        'ingredient_unit': dish_ingredient.ingredient.unit.designation
                    }

            )
        context['ingredient_formset'] = IngredientFormset(initial=ingredient_data)
        context['ingredient_len'] = len(ingredient_data) - 1
        return context

    def post(self, request, pk: int, *args, **kwargs):
        dish = get_object_or_404(Dish, pk=pk)
        dish_form = DishForm(request.POST, instance=dish)
        if dish_form.is_valid():
            dish_form.save()
        # TODO: handle exceptions: show errors if not valid
        ingredient_formset = IngredientFormset(request.POST)
        if ingredient_formset.is_valid():
            dish.save_ingredients(ingredient_formset.cleaned_data)

        # if ingredient_formset.is_valid():
        #     dish = dish_form.dish_save(ingredient_formset.cleaned_data)
        # TODO: change to dish with argument dish_id
        # TODO: show errors if not valid
        return redirect(dish)
