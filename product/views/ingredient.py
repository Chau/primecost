from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ..models import Ingredient


def ingredient_list_json(request):
    ingredients_json = Ingredient.search_ingredient()
    return JsonResponse(ingredients_json, safe=False)


def ingredient_delete_json(request, pk, *args, **kwargs):
    Ingredient.objects.filter(pk=pk).delete()
    return JsonResponse({'status': 'ok'}, safe=False)


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
        return reverse('ingredient_edit', args={'pk': self.object.id})


class IngredientDeleteView(DeleteView):
    model = Ingredient

