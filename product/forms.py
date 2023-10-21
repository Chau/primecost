import typing as t

from django import forms

from product.models import Dish


class IngredientForm(forms.Form):
    ingredient_id = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'ingredientId'}))
    ingredient_name = forms.CharField(label='Наименование', widget=forms.TextInput(attrs={'id': 'ingredientName'}))
    ingredient_amount = forms.FloatField(label='Количество', widget=forms.TextInput(attrs={'id': 'ingredientAmount'}))
    ingredient_unit = forms.CharField(label='Измерение', widget=forms.TextInput(attrs={'id': 'ingredientUnit'}))

    class Meta:
        # model = Ingredient
        fields = ('ingredient_id', 'ingredient_name', 'ingredient_amount', 'ingredient_unit')


IngredientFormset = forms.formset_factory(
            form=IngredientForm,
            extra=0
        )


class DishForm(forms.ModelForm):

    def dish_save(self, ingredients_data: t.List[t.Dict]):
        if self.is_valid():
            dish = self.save()
            # remove empty items
            while ingredients_data.count({}) > 0:
                ingredients_data.remove({})
            dish.save_ingredients(ingredients_data)
            return dish
        return

    def is_valid(self):
        return super(DishForm, self).is_valid()

    class Meta:
        model = Dish
        exclude = ('ingredient', )

