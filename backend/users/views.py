from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from .models import User
from .serializers import UserCreateSerializer, SetPasswordSerializer


class UserCreateViewSet(viewsets.ModelViewSet):
    """Creating User"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class SetPasswordViewSet(ViewSet):
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
