class SubscribeMixin:
    """
    Описывает поле is_subscribed.
    Возвращает набор подписок автора."""
    def get_is_subscribed(self, obj):
        request = self.context['request']
        if request.user == obj:
            return False
        else:
            return obj.subscribers.all().filter(user=request.user.id).exists()


class ShoppingFavoriteMixin:
    """
    Миксин для поверки полей:
    - Находится ли рецепт в избранном.
    - Находится ли рецепт в списке покупок.
    """
    def get_is_favorited(self, obj):
        """Провека избранных рецептов пользователя."""
        request = self.context['request']
        user = request.user
        value = (
            False if user.is_anonymous
            else user.favorite_recipes.all().filter(id=obj.id).exists()
        )
        return value

    def get_is_in_shopping_cart(self, obj):
        """Проверка списка покупок пользователя."""
        request = self.context['request']
        user = request.user
        value = (
            False if user.is_anonymous
            else user.recipes_in_cart.all().filter(id=obj.id).exists()
        )
        return value
