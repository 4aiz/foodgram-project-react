from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from rest_framework import status

from recipe.models import Follow
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_subscribed']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=150, default=None)
    current_password = serializers.CharField(max_length=150, default=None)

    class Meta:
        model = User
        fields = ['new_password', 'current_password']
