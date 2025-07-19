import django_filters

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(django_filters.FilterSet):
    """Фильтр для поиска ингредиентов."""

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
        help_text='Название ингредиента (по начальным буквам)',
    )

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(django_filters.FilterSet):
    """
    Кастомный фильтр рецепта по избранному, автору, списку покупок и тегам.
    """
    is_favorited = django_filters.NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'author', 'is_in_shopping_cart', 'tags']

    def _filter_by_user_relation(self, queryset, relation_name: str, value):
        """Фильтрует queryset в зависимости от пользователя."""
        user = self.request.user
        if user.is_authenticated and value:
            return queryset.filter(**{relation_name: user})
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        """Фильтрует по рецептам в избранном"""
        return self._filter_by_user_relation(queryset, 'is_favorited', value)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        """Фильтрует по рецептам в списке покупок."""
        return self._filter_by_user_relation(
            queryset, 'is_in_shopping_cart', value
        )
