from django.contrib import admin

from users.models import FoodgramUser, Subscription


@admin.register(FoodgramUser)
class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'avatar',
    )
    search_fields = ('email', 'first_name',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'user',
    )
    search_fields = ('author', 'user',)


admin.site.empty_value_display = 'Не задано'
