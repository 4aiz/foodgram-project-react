import base64

import webcolors
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipe.models import Tag, Ingredient, Recipe, Follow, Favorite, ShoppingCart


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


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tag = TagSerializer(
        required=True,
        many=True,
    )
    ingredients = IngredientSerializer(
        # required=True,
        read_only=True,
        many=True,
    )

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.ingredients = validated_data.get(
    #         'ingredients', instance.ingredients
    #     )
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
    #
    #     if 'tags' in validated_data:
    #         tags_data = validated_data.pop('tags')
    #         lst = []
    #         for tag in tags_data:
    #             current_tag, status = Tag.objects.get_or_create(
    #                 **tag
    #             )
    #             lst.append(current_tag)
    #         instance.tags.set(lst)
    #
    #     instance.save()
    #     return instance

    class Meta:
        model = IngredientSerializer
        fields = ('id', 'author', 'tags', 'name', 'image', 'description', 'ingredients', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


# class ReviewSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='username',
#         default=serializers.CurrentUserDefault()
#     )
#     title = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='name'
#     )
#
#     def validate(self, data):
#         request = self.context['request']
#         author = request.user
#         title_id = self.context['view'].kwargs.get('title_id')
#         title = get_object_or_404(Title, pk=title_id)
#         if request.method == 'POST':
#             if Review.objects.filter(title=title, author=author).exists():
#                 raise ValidationError('Вы не можете добавить'
#                                       ' ещё один отзыв на произведение')
#         return data
#
#     class Meta:
#         model = Review
#         fields = '__all__'
