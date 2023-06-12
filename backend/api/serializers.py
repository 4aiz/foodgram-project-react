from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipe.models import Tag, Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Tag


class RecipeSerializer(serializers.ModelSerializer):
    tag = TagSerializer(
        read_only=True
    )
    ingredient = IngredientSerializer(
        many=True,
        read_only=True
    )
    # rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = IngredientSerializer
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        read_only_fields = ('id',)


class RecipeCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        model = Recipe


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить'
                                      ' ещё один отзыв на произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'
