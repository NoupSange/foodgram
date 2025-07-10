from api.serializers.custom_fields import Base64ImageField
from api.serializers.custom_mixins import SubscribeMixin
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSerializer
from recipes.models import Recipe
from rest_framework import serializers

User = get_user_model()


class UserSerializer(DjoserUserSerializer, SubscribeMixin):
    """Сериализатор данных пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )

    def get_is_subscribed(self, obj):
        """Подписан ли текущий пользователь на этого."""
        request = self.context.get('request')
        if request.user == obj:
            return False
        else:
            return obj.subscribers.all().filter(user=request.user.id).exists()


class AvatarSerializer(serializers.Serializer):
    """
    Сериализует и десереализует фото автара пользователя
    в кодировке Base64.
    """
    avatar = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ('avatar',)

    def update(self, instance, validated_data):
        """Обновляет фото пользователя при PUT запросе."""
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class SubscriptionRecipeSerializer(serializers.ModelSerializer):
    """
    Показывает инормацию о рецептах автора,
    """
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscriptionSerializer(UserSerializer, SubscribeMixin):
    """Сериализатор рецептов """
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar',
        )

    def get_recipes(self, obj):
        """
        Пагинация по параметру запоса recipes_limit.
        Лимитирует количество показываемых рецептов автора.
        """
        request = self.context.get('request')
        limit = (
            request.query_params.get('recipes_limit')
            if request else None
        )
        queryset = obj.recipes.all()
        if limit and limit.isdigit():
            queryset = queryset[:int(limit)]
        return SubscriptionRecipeSerializer(queryset, many=True).data
