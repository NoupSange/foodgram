from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.serializers.users import (AvatarSerializer, SubscriptionSerializer,
                                   UserSerializer)
from api.views.pagintaion import LimitPagination
from users.models import Subscription

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет пользователей."""
    serializer_class = UserSerializer
    pagination_class = LimitPagination

    def get_serializer_class(self):
        if self.action == "me":
            return UserSerializer
        if self.action == "me_avatar":
            return AvatarSerializer
        elif self.action in ("subscriptions", "subscribe"):
            return SubscriptionSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        """
        Объявляет доступ для всех к списку пользователей
        или созданию нового пользователя. Остальные permissioins
        наследуются от родительского класса.
        """
        if self.action in ("list", "create"):
            self.permission_classes = [AllowAny]
        elif self.action == "retrieve":
            return [AllowAny()]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    @action(
        methods=["get"],
        detail=False,
    )
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.request.user)
        return Response(serializer.data)

    @action(
        methods=["put"],
        url_path="me/avatar",
        detail=False,
    )
    def me_avatar(self, request):
        """Добавление аватара для текущего пользователя."""

        if "avatar" not in request.data:
            return Response(
                {"avatar": "Обязательное поле"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @me_avatar.mapping.delete
    def delete_me_avatar(self, request):
        """Удаялет аватар пользователя."""
        user = request.user
        if user.avatar:
            user.avatar = ""
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        pagination_class=LimitPagination,
    )
    def subscriptions(self, request):
        """
        Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        """
        queryset = User.objects.filter(
            subscribers__user=request.user
        ).annotate(
            recipes_count=Count("recipes")
        ).order_by("username")

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page,
            many=True,
            context={"request": request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
    )
    def subscribe(self, request, id=None):
        """Подписаться на пользователяПодписаться на пользователя."""
        user = request.user
        author = get_object_or_404(
            User.objects.annotate(recipes_count=Count("recipes")),
            id=id,
        )

        if author == user:
            return Response(
                {"detail": "Нельзя подписаться на себя."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription, created = Subscription.objects.get_or_create(
            user=user,
            author=author,
        )
        if not created:
            return Response(
                {"detail": "Вы уже подписаны на этого пользователя."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            author,
            context={"request": request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        """Отписаться от пользователя."""
        user = request.user
        author = get_object_or_404(User, id=id)
        deleted_count, _ = user.subscriptions.filter(
            author=author,
        ).delete()

        if deleted_count == 0:
            return Response(
                {"detail": "Вы не подписаны на этого пользователя."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
