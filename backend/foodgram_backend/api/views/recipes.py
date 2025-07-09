from recipes.models import Tag, Recipe, RecipeIngredient, Ingredient, ShoppingCart, Favorite
from django_filters.rest_framework import DjangoFilterBackend
from api.serializers.recipes import (
    TagSerializer,
    IngredientSerializer,
    RecipeCreateUpdateSerializer,
    RecipeListSerializer,
    FavoriteRecipeSerializer
)
from api.views.filters import RecipeFilter, IngredientFilter
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import action
from api.views.pagintaion import LimitPagination
from api.views.permissioins import IsAuthorOrReadOnly
User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращает список тэгов или отдельный тэг."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращает список тэгов или отдельный тэг."""
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter

    def get_queryset(self):
        return Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend,]
    filterset_class = RecipeFilter
    pagination_class = LimitPagination

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            self.serializer_class = RecipeCreateUpdateSerializer
        else:
            self.serializer_class = RecipeListSerializer
        return super().get_serializer_class()

    @action(
        detail=True,
        methods=['get'],
        url_path='get-link',
    )
    def get_link(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        short_url = request.build_absolute_uri(
            reverse(
                'redirect_short_link',
                kwargs={'short_code': recipe.short_code},
            )
        )
        return Response(
            {'short-link': short_url},
            status=status.HTTP_200_OK,
        )

    def _create_relation(self, request, pk, model):
        """
        Добавляет связь между пользователем и рецептом в таблице модели.
        """
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        obj, created = model.objects.get_or_create(user=user, recipe=recipe)
        if not created:
            return Response(
                {'detail': f'Рецепт уже в {model._meta.verbose_name}.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = FavoriteRecipeSerializer(
            recipe,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _remove_relation(self, request, pk, model):
        """
        Удаляет связь между пользователем и рецептом в таблице модели.
        """
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        deleted, _ = model.objects.filter(
            user=user,
            recipe=recipe,
        ).delete()
        if deleted == 0:
            return Response(
                {'detail':
                 f'Рецепта отсутствует в {model._meta.verbose_name}.'
                 },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
    )
    def shopping_cart(self, request, pk=None):
        """Добавляет рецепт в избранное авторизованного пользователя."""
        return self._create_relation(request, pk, ShoppingCart)

    @shopping_cart.mapping.delete
    def remove_from_cart(self, request, pk=None):
        return self._remove_relation(request, pk, ShoppingCart)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__shoppingcart_set__user=user)
            .values(
                'ingredient__name',
                'ingredient__measurement_unit',
            )
            .annotate(total_amount=Sum('amount'))
            .order_by('ingredient__name')
        )
        lines = [
            f"{item['ingredient__name']} "
            f"({item['ingredient__measurement_unit']}) — "
            f"{item['total_amount']}"
            for item in ingredients
        ]
        content = '\n'.join(lines)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        return self._create_relation(request, pk, Favorite)

    @favorite.mapping.delete
    def remove_from_favorite(self, request, pk=None):
        return self._remove_relation(request, pk, Favorite)
