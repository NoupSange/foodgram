from api.views import recipes, users
from django.urls import include, path, re_path
from rest_framework import routers

api_v1 = routers.DefaultRouter()
api_v1.register(r'users', users.UserViewSet, basename='users')
api_v1.register(r'tags', recipes.TagViewSet, basename='tags')
api_v1.register(r'recipes', recipes.RecipeViewSet, basename='recipes')
api_v1.register(
    r'ingredients', recipes.IngredientViewSet, basename='ingredients'
)

urlpatterns = [
    path('', include(api_v1.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
