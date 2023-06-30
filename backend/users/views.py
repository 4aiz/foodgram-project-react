from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from recipe.models import Follow

from .models import User
from .serializers import (FollowSerializer, SetPasswordSerializer,
                          UserCreateSerializer)


class UserCreateViewSet(viewsets.ModelViewSet):
    """Creating User"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, *args, **kwargs):
        following = get_object_or_404(User, id=request.data['id'])
        serializer = FollowSerializer(
            following, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            Follow.objects.create(user=request.user, following=following)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            Follow.objects.filter(
                author=following,
                user=request.user
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        self.queryset = Follow.objects.filter(user=user)

    # def get_permissions(self):
    #     if self.action == 'list':
    #         self.permission_classes = [AllowAny, ]
    #     else:
    #         self.permission_classes = [IsAuthenticated, ]
    #     return [permission() for permission in self.permission_classes]


class SetPasswordViewSet(ViewSet):
    """User change password"""
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            current_password = serializer.validated_data['current_password']

            user = request.user
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                return Response(
                    {'message': 'Password has been changed successfully.'},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'message': 'Current password is incorrect.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
