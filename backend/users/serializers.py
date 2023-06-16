from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer

from .models import User


class UserDetailSerializer(UserSerializer):
    # first_name = serializers.CharField(max_length=150)
    # last_name = serializers.CharField(max_length=150)

    def is_subscribed(self):
        pass

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
        read_only_fields = ('id', )


class CreateUserSerializer(UserCreateSerializer):

    def perform_create(self, validated_data):
        ...

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',
                  'confirmation_code']
