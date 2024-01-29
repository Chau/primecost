from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ..models import Ingredient


def ingredient_list_json(request):
    ingredients_json = Ingredient.search_ingredient()
    return JsonResponse(ingredients_json, safe=False)


def ingredient_delete_json(request, pk, *args, **kwargs):
    try:
        ingredient = Ingredient.objects.get(pk=pk)
    except Ingredient.DoesNotExist:
        result = {'status': 'error', 'message': 'Ингредиент не существует в базе'}
        return JsonResponse(result, safe=False)

    dishes = ingredient.search_dishes()
    if not dishes:
        Ingredient.objects.filter(pk=pk).delete()
        result = {'status': 'ok'}
    else:
        dishes_message = (
            'Невозможно удалить ингредиент "{}", так как он является частью следующих блюд: \n{}'
                          .format(
                                ingredient.name,
                                      '\n'.join([dish.name for dish in dishes]))
        )
        result = {'status': 'error', 'message': dishes_message}
    return JsonResponse(result, safe=False)


class IngredientListView(ListView):
    model = Ingredient
    context_object_name = 'ingredients'

    def get_queryset(self):
        return Ingredient.objects.select_related().all().order_by('-pk')


class IngredientDetailView(DetailView):
    model = Ingredient


class IngredientCreateView(CreateView):
    model = Ingredient
    template_name = 'product/ingredient_form_create.html'
    success_url = '/ingredient/create'
    fields = ('name', 'description', 'unit', 'price')


class IngredientUpdateView(UpdateView):
    model = Ingredient
    template_name = 'product/ingredient_form_update.html'
    fields = ('name', 'description', 'unit', 'price')

    def get_success_url(self):
        return reverse('ingredient_edit', kwargs={'pk': self.object.id})


class IngredientDeleteView(DeleteView):
    model = Ingredient

