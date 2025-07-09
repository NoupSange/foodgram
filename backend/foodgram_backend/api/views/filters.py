import django_filters
from recipes.models import Recipe, Ingredient
from django.db.models import Q

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
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        help_text='Фильтрация по слагам тегов',
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

    def filter_tags(self, queryset, name, value):
        """Фильтрует по тегам."""
        if not isinstance(value, list):
            value = [value]
        query = Q()
        for tag in value:
            query |= Q(tags__slug=tag)
        return queryset.filter(query).distinct()