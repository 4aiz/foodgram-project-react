from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from api.pagination import CustomLimitPagination
from api.permissions import IsAuthenticatedAuthorOrAdmin
from recipe.models import Follow

from .models import User
from .serializers import (SetPasswordSerializer, SubscriptionSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """User api"""

    def get_queryset(self):
        if self.action == 'subscribe':
            return Follow.objects.filter(user=self.request.user)
        else:
            return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'subscribe':
            return SubscriptionSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action == 'subscribe':
            return [IsAuthenticated()]
        elif self.action in ('create', 'list'):
            return [AllowAny()]
        else:
            return super().get_permissions()

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=["POST", "DELETE"])
    def subscribe(self, request, pk):
        following = get_object_or_404(User, id=pk)
        user = request.user
        serializer = SubscriptionSerializer(
            following, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            if Follow.objects.filter(user=user, following=following).exists():
                return Response(
                    {'errors': 'Невозможно подписаться дважды'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                Follow.objects.create(user=user, following=following)
                return Response(
                    {'detail': 'Вы подписались на автора'},
                    status=status.HTTP_201_CREATED
                )
        else:
            try:
                Follow.objects.filter(
                    user=user,
                    following=following,
                ).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Follow.DoesNotExist:
                return Response(
                    {'errors': 'Вы не подписаны на автора'},
                    status=status.HTTP_400_BAD_REQUEST
                )


class SubscriptionListViewSet(mixins.ListModelMixin,
                              GenericViewSet):
    pagination_class = CustomLimitPagination
    permission_classes = [IsAuthenticatedAuthorOrAdmin]
    serializer_class = SubscriptionSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^following__user', )

    def get_queryset(self):
        user = self.request.user
        qs = User.objects.filter(following__user=user)
        return qs


class SetPasswordViewSet(ViewSet):
    """User change password"""

    def create(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'errors': 'Пользователь не авторизован'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = SetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            current_password = serializer.validated_data['current_password']

            if new_password == current_password:
                return Response(
                    {'detail': 'Новый пароль совпадает с текущим'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                return Response(
                    {'detail': 'Пароль успешно сменен'},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'detail': 'Неверный пароль'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
