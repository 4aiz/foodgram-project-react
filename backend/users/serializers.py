from rest_framework import serializers

from recipe.models import Follow, Recipe

from .models import User


class RecipeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'cooking_time'
        )
        read_only_fields = (
            'id', 'name', 'image', 'cooking_time'
        )


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.id:
            return False
        return Follow.objects.filter(user=user, following=obj).exists()

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


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        request = self.context['request']
        recipes = Recipe.objects.filter(author=obj).all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit and isinstance(recipes_limit, str):
            recipes_limit = int(recipes_limit)
            recipes = recipes[:recipes_limit]
        return RecipeShortSerializer(
            recipes,
            many=True,
            context={'request': request}
        ).data

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Follow.objects.filter(user=user, following=obj).exists()

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author=obj).all()
        return len(recipes)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'is_subscribed', 'recipes', 'recipes_count',
            'username', 'first_name', 'last_name'
        )
        read_only_fields = (
            'email', 'id', 'is_subscribed', 'recipes', 'recipes_count',
            'username', 'first_name', 'last_name'
        )


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
