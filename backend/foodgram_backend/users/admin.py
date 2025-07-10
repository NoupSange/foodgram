from django.contrib import admin
from users.models import FoodgramUser, Subscription

admin.site.register(FoodgramUser)
admin.site.register(Subscription)
