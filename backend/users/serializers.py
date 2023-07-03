from rest_framework import serializers

from recipe.models import Follow

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',
                  'first_name', 'last_name', 'is_subscribed')
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


class UserFollowSerializer(serializers.ModelSerializer):
    # recipes = serializers.SerializerMethodField()
    #
    # def get_recipes(self):
    #     return ['Тут должны быть рецепты']

    class Meta:
        model = Follow
        # fields = (
        #     'id', 'username', 'email',
        #     'first_name', 'last_name', 'is_subscribed', 'recipes'
        # )
        fields = ('id', 'user', 'following')


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
