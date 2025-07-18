from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(
    Favorite,
    ShoppingCart
)
class FavoriteShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('user__username', 'recipe__name',)


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)


class IngredienInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    inlines = (
        IngredienInline,
    )
    list_display = (
        'name',
        'author',
        'cooking_time',
        'favorite_count'
    )
    filter_horizontal = ('tags',)
    search_fields = ('name', 'author__username')
    list_filter = ('tags',)
    readonly_fields = ('favorite_count', )

    def favorite_count(self, obj):
        return obj.favorite_set.count()
    favorite_count.short_description = 'Количество добавлений в избранное'


admin.site.empty_value_display = 'Не задано'
