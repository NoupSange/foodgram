from rest_framework import serializers

class SubscribeMixin():
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user == obj:
            return False
        else:
            return obj.subscribers.all().filter(user=request.user.id).exists()

class ShoppingFavoriteMixin():
    """
    Миксин для проверки полей is_favorited
    и is_in_shopping_cart рецепта.
    """
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        value = (
            False if user.is_anonymous
            else user.favorite_recipes.all().filter(id=obj.id).exists()
        )
        return value

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        value = (
            False if user.is_anonymous
            else user.recipes_in_cart.all().filter(id=obj.id).exists()
        )
        return value
