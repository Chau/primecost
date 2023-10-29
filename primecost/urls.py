"""
URL configuration for primecost project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from product.views import (DishDetailView, DishListView, DishCreateView, DishUpdateView,
                           dish_delete_json,
                           IngredientListView, IngredientDetailView, IngredientCreateView, IngredientUpdateView,
                           IngredientDeleteView,
                           ingredient_list_json, ingredient_delete_json)

urlpatterns = [
    path('dish/<int:pk>', DishDetailView.as_view(), name='dish_detail'),
    path('dish/list', DishListView.as_view(), name='dish_list'),
    path('dish/create', DishCreateView.as_view(), name='dish_create'),
    path('dish/<int:pk>/edit', DishUpdateView.as_view(), name='dish_edit'),
    path('dish/<int:pk>/delete_json', dish_delete_json, name='dish_delete_json'),
    path('ingredient/<int:pk>', IngredientDetailView.as_view(), name='ingredient_detail'),
    path('ingredient/list', IngredientListView.as_view(), name='ingredient_list'),
    path('ingredient/list_json', ingredient_list_json, name='ingredient_list_json'),
    path('ingredient/create', IngredientCreateView.as_view(), name='ingredient_create'),
    path('ingredient/<int:pk>/edit', IngredientUpdateView.as_view(), name='ingredient_edit'),
    path('ingredient/<int:pk>/delete', IngredientDeleteView.as_view(), name='ingredient_delete'),
    path('ingredient/<int:pk>/delete_json', ingredient_delete_json, name='ingredient_delete_json'),
    path('admin/', admin.site.urls),
]
