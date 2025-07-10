import shortuuid
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from recipes.constants import (MAX_COOKING_TIME, MIN_COOKING_TIME,
                               UUID_MAX_LENGTH)

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиента для рецепта."""

    name = models.CharField(
        max_length=128,
        verbose_name="Название ингредиента"
    )

    measurement_unit = models.CharField(
        max_length=64,
        verbose_name="Единица измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.measurement_unit})"


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название тега"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Слаг тега"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Recipe(models.Model):
    """
    Модель рецепта.

    Атрибуты:
        author (ForeignKey): Автор публикации (пользователь).
        name (CharField): Название рецепта.
        image (ImageField): Картинка рецепта.
        description (TextField): Текстовое описание рецепта.
        ingredients (ManyToManyField): Ингредиенты для приготовления.
        tags (ManyToManyField): Теги рецепта.
        cooking_time (PositiveIntegerField): Время приготовления в минутах.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта"
    )
    name = models.CharField(
        max_length=256,
        verbose_name="Название рецепта"
    )
    image = models.ImageField(
        upload_to="recipes/",
        verbose_name="Картинка рецепта"
    )
    used_ingredients = models.ManyToManyField(
        Ingredient,
        related_name="used_in_recipes",
        verbose_name="Ингредиенты",
        through='RecipeIngredient',
    )
    text = models.TextField(verbose_name='Описание рецепта')
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        verbose_name="Теги"
    )
    is_favorited = models.ManyToManyField(
        User,
        related_name="favorite_recipes",
        verbose_name="В избранном",
        through='Favorite'
    )
    is_in_shopping_cart = models.ManyToManyField(
        User,
        related_name="recipes_in_cart",
        verbose_name="В коорзине",
        through='ShoppingCart',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name="Время приготовления (в минутах)",
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                f"Время приготовления не может быть"
                f"меньше {MIN_COOKING_TIME} минут."
            ),
            MaxValueValidator(
                MAX_COOKING_TIME,
                f"Время приготовления не может быть"
                f"меньше {MAX_COOKING_TIME} минут."
            )
        ]
    )

    short_code = models.CharField(
        max_length=UUID_MAX_LENGTH,
        unique=True,
        default=shortuuid.uuid,
        verbose_name='Короткий код',
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Промежуточная модель для связи рецептов и ингредиентов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name="Рецепт"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name="Ингредиент",
    )
    amount = models.PositiveIntegerField(
        verbose_name="Количество",
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                f"Время приготовления не может быть"
                f"меньше {MIN_COOKING_TIME} минут."
            ),
            MaxValueValidator(
                MAX_COOKING_TIME,
                f"Время приготовления не может быть"
                f"меньше {MAX_COOKING_TIME} минут."
            )
        ]
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_recipe'
            )
        ]

    def __str__(self):
        return f"{self.ingredient.name} в {self.recipe.name}"


class UserRecipeRelation(models.Model):
    """Абстрактная базовая модель для связи пользователя и рецепта."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_%(class)s',
            )
        ]


class Favorite(UserRecipeRelation):
    """Модель для хранения избранных рецептов пользователя."""

    class Meta(UserRecipeRelation.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class ShoppingCart(UserRecipeRelation):
    """Модель списка покупок."""

    class Meta(UserRecipeRelation.Meta):
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.recipe} в списке покупок {self.user}.'
