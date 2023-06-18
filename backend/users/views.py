from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import User
# from api.permissions import AdminPermission
# from api.pagination import Pagination
from .serializers import UserDetailSerializer


class UserCreateViewSet(viewsets.ModelViewSet):
    """Creating User"""
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='set_password')
    def set_password(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

            if not check_password(current_password, user.password):
                return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password changed successfully.'})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def get_permissions(self):
        if self.action in ['me', 'set_password']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
