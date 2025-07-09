from django.contrib import admin
from recipes.models import Ingredient, Tag, Recipe, RecipeIngredient, Favorite, ShoppingCart


@admin.register(
    Ingredient,
    Tag,
    Recipe,
    RecipeIngredient,
    Favorite,
    ShoppingCart
)
class RecipesAdmin(admin.ModelAdmin):
    pass
