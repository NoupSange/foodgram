from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


EMAIL_LENGTH = 254
DEFAULT_LENGTH = 150


class FoodgramUser(AbstractUser):
    """Кастомная модель пользователя."""
    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        unique=True,
        verbose_name='Адрес электронной почты',
    )

    username = models.CharField(
        max_length=DEFAULT_LENGTH,
        unique=True,
        validators=[AbstractUser.username_validator],
    )

    first_name = models.CharField(
        max_length=DEFAULT_LENGTH,
        verbose_name='Имя',
    )

    last_name = models.CharField(
        max_length=DEFAULT_LENGTH,
        verbose_name='Фамилия'
    )
    is_subscribed = models.ManyToManyField(
        'self',
        through='Subscription',
    )

    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        ordering = ['email']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписки пользователя на автора."""

    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_subscription',
            ),
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
