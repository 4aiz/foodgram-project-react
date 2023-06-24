import base64

import webcolors
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipe.models import Tag, Ingredient, Recipe, Follow, Favorite, ShoppingCart, RecipeIngredient
from users.serializers import UserCreateSerializer


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        for tag in data:
            try:
                color = webcolors.hex_to_name(data.get(tag))
            except ValueError:
                raise serializers.ValidationError('Для этого цвета нет имени')
            return color


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', )
        read_only_fields = ('measurement_unit', )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'ingredient', 'amount')
        # read_only_fields = ('id', )


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(many=True,)
    text = serializers.CharField(source='description')
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        print(ingredients)
        for ingredient in ingredients:
            print(ingredient)
            amount = ingredient.pop('amount')  # После этого словарь пуст
            current_ingredient, status = Ingredient.objects.get_or_create(**ingredient)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=current_ingredient, amount=amount)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)

        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)

        if 'ingredients' not in validated_data:
            instance.save()
            return instance

        ingredients_data = validated_data.pop('ingredients')
        lst = []
        for ingredient in ingredients_data:
            current_ingredient, status = Ingredient.objects.get_or_create(
                **ingredient
            )
            lst.append(current_ingredient)
        instance.achievements.set(lst)

        instance.save()
        return instance

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('author',)


class RecipeDetailSerializer(serializers.ModelSerializer):
    author = UserCreateSerializer()
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    ingredients = IngredientSerializer(
        many=True,
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    text = serializers.CharField(source='description')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(user=user, recipe=obj).exists()
        return False

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_favorited'] = self.get_is_favorited(instance)
        representation['is_in_shopping_cart'] = self.get_is_in_shopping_cart(instance)
        return representation

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('author', )


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'user', 'recipe')


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'recipe')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'user', 'following')
