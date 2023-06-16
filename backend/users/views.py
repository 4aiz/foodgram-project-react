from djoser.views import UserViewSet

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from .models import User
from api.permissions import AdminPermission
from .serializers import (UserDetailSerializer,
                          CreateUserSerializer, )


class UserViewSet(UserViewSet):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()


@method_decorator(csrf_protect, name='dispatch')
class ProfileActions(APIView):
    def get_permissions(self):
        if self.kwargs.get('username', '') == 'me':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AdminPermission]

        return super().get_permissions()

    def get(self, request, username):
        try:
            if username == 'me':
                user = request.user
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, username):
        if username == 'me':
            user = request.user
            serializer = UserDetailSerializer(user,
                                             data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.get(username=username)
            serializer = UserDetailSerializer(user,
                                            data=request.data,
                                            partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        if username == 'me':
            return Response('Method not allowed',
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = get_object_or_404(User, username=username)

        user.delete()
        return Response('User deleted', status=status.HTTP_204_NO_CONTENT)
