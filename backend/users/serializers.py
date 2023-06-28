from django.contrib.auth.hashers import check_password
from rest_framework import serializers, status

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


class FollowSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        subscription = Follow.objects.create(
            user=self.context['request'].user,
            following=validated_data['following']
        )
        subscription.save()
        return subscription

    class Meta:
        model = Follow
        fields = ('user', 'following')


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
