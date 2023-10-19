from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from ..models import Ingredient


def ingredient_list_json(request):
    ingredients_json = Ingredient.search_ingredient()
    return JsonResponse(ingredients_json, safe=False)


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
