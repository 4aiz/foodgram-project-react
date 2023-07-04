from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from recipe.models import Follow

from .models import User
from .serializers import (SetPasswordSerializer, UserCreateSerializer,
                          UserFollowCreateSerializer, UserFollowReadSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """User api"""

    def get_queryset(self):
        if self.action == 'subscriptions':
            user = self.request.user
            return Follow.objects.filter(user=user)
        elif self.action == 'subscribe':
            return Follow.objects.all()
        else:
            return User.objects.all()

    def get_serializer_class(self):
        if self.action in ('subscribe', 'subscriptions'):
            return UserFollowCreateSerializer
        else:
            return UserCreateSerializer

    def get_permissions(self):
        if self.action in ('subscribe', 'subscriptions'):
            return [IsAuthenticated()]
        elif self.action in ('create', 'list'):
            return [AllowAny()]
        else:
            return super().get_permissions()

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=["post", "delete"])
    def subscribe(self, request, pk):
        following = get_object_or_404(User, id=pk)
        user = request.user
        serializer = UserFollowCreateSerializer(
            following, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "post":
            Follow.objects.create(user=user, following=following)
            return Response({'detail': 'Created'}, status=status.HTTP_201_CREATED)
        else:
            Follow.objects.filter(
                following=following,
                user=user
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        subscriptions = Follow.objects.filter(user=request.user)
        return Response(UserFollowReadSerializer(subscriptions, many=True).data)


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
