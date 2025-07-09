from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import FoodgramUser, Subscription

admin.site.register(FoodgramUser)
admin.site.register(Subscription)
