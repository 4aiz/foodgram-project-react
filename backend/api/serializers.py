import base64

import webcolors
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipe.models import (Ingredient,
                           Recipe,
                           RecipeIngredient,
                           Tag,
                           Favorite,
                           ShoppingCart)
from users.serializers import UserSerializer


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
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('name', 'measurement_unit', 'amount')


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
    amount = serializers.IntegerField(write_only=True, min_value=1)
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'id', 'amount',)


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    text = serializers.CharField(source='description')
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = RecipeIngredientCreateSerializer(many=True)

    def validate_cooking_time(self, value):
        if not value or value <= 0:
            raise serializers.ValidationError(
                'Минимальное время готовки - 1 минута'
            )
        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                'Нельзя создать рецепт без ингредиентов'
            )

        ingredients = [x['ingredient'].name for x in value]
        if len(ingredients) != len(set(ingredients)):
            raise serializers.ValidationError(
                'Нельзя создать рецепт с повторяющимися ингредиентами'
            )
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient.get('ingredient'),
                amount=ingredient.get('amount'))
            for ingredient in ingredients
        ]

        RecipeIngredient.objects.bulk_create(recipe_ingredients)
        return recipe

    def update(self, instance, validated_data):
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)

        if 'ingredients' in validated_data:
            instance.ingredients.clear()
            ingredients_data = validated_data.pop('ingredients')
            recipe_ingredients = [
                RecipeIngredient(
                    recipe=instance,
                    ingredient=ingredient.get('ingredient'),
                    amount=ingredient.get('amount'))
                for ingredient in ingredients_data
            ]
            RecipeIngredient.objects.bulk_create(recipe_ingredients)

        instance.save()
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        self.fields.pop('ingredients')
        self.fields['tags'] = TagSerializer(many=True)
        representation = super().to_representation(instance)

        representation['ingredients'] = RecipeIngredientReadSerializer(
            RecipeIngredient.objects.filter(recipe=instance).all(), many=True
        ).data
        return representation

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('author',)


class RecipeReadlSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    text = serializers.CharField(source='description')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(
                recipe=obj,
                user=user
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                recipe=obj,
                user=user
            ).exists()
        return False

    def get_ingredients(self, obj):
        return RecipeIngredientReadSerializer(
            RecipeIngredient.objects.filter(recipe=obj).all(), many=True).data

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('author', )
