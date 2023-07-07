from django.contrib import admin
from users.models import User

from .models import Favorite, Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'in_favorite')
    list_filter = ('author', 'name', 'tags')

    def in_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).all().count()


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('username', 'email')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
