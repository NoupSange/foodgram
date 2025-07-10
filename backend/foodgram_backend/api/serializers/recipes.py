from api.serializers.custom_fields import Base64ImageField
from api.serializers.custom_mixins import ShoppingFavoriteMixin
from api.serializers.users import UserSerializer
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError

User = get_user_model()


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор избранных рецептов."""

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'slug'
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингредиента с дополнительным
    полем количества ингредиента.
    """

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeListSerializer(serializers.ModelSerializer, ShoppingFavoriteMixin):
    """Сериализатор списка рецептов."""
    tags = TagSerializer(many=True)
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class RecipeCreateUpdateSerializer(serializers.ModelSerializer,
                                   ShoppingFavoriteMixin):
    """Сериализатор для создания или обновления рецепта."""
    ingredients = RecipeIngredientSerializer(many=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('id', 'is_favorited', 'is_in_shopping_cart')

    def _check_dublicates_utility(self, ingredients, tags) -> None:
        """
        Валидирует наличие дубликатов
        тегов и рецептов при создании рецепта.
        """
        seen_items = set()
        for ingredient in ingredients:
            current_ingredient = ingredient["id"]
            if ingredient["id"] in seen_items:
                raise ValidationError(
                    f"{current_ingredient}",
                    "повторяется в рецепте."
                )
            seen_items.add(current_ingredient)
        for tag in tags:
            if tag in seen_items:
                raise ValidationError(
                    f"{tag}",
                    "повторяется в рецепте."
                )
            seen_items.add(tag)

    def _recipe_ingredient_utility(self, recipe_ingredients, recipe):
        """Создает связь рецепта и ингридента в промежуточной таблице."""
        for recipe_ingredient in recipe_ingredients:
            current_ingredient = recipe_ingredient["id"]
            RecipeIngredient.objects.get_or_create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=recipe_ingredient["amount"]
            )

    def _pop_data_utility(self, validated_data):

        try:
            recipe_ingredients = validated_data.pop('ingredients')
            if not recipe_ingredients:
                raise ValidationError(
                    'Необходимо указать хотя бы 1 ингредиент.'
                )
            tags = validated_data.pop('tags')
            return recipe_ingredients, tags
        except Exception as e:
            raise ValidationError(f'Поле {e} не заполнено.')

    @atomic
    def create(self, validated_data):
        """
        Создает связь нового рецепта с ингредиентов(новыи или существующим).
        """
        recipe_ingredients, tags = self._pop_data_utility(validated_data)
        self._check_dublicates_utility(recipe_ingredients, tags)
        user = self.context['request'].user
        new_recipe = Recipe.objects.create(author=user, **validated_data)
        self._recipe_ingredient_utility(recipe_ingredients, new_recipe)
        new_recipe.tags.set(tags)
        return new_recipe

    @atomic
    def update(self, recipe, validated_data):
        """Обновляет данные рецепта.
        Очищает связанные с рецептом теги и ингридиенты,
        после чего заполняет БД новыми значениями."""
        user = self.context['request'].user
        if user != recipe.author:
            raise PermissionDenied
        recipe_ingredients, tags = self._pop_data_utility(validated_data)
        self._check_dublicates_utility(recipe_ingredients, tags)
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        recipe.tags.set(tags)
        self._recipe_ingredient_utility(recipe_ingredients, recipe)
        recipe = super().update(recipe, validated_data)
        recipe.save()
        return recipe

    def to_representation(self, instance):
        """Преобразует список ID тегов в список объектов тегов."""
        representation = super().to_representation(instance)
        tags = instance.tags.all()
        representation['tags'] = TagSerializer(tags, many=True).data
        return representation
