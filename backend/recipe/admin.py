from django.contrib import admin

from .models import Recipe, Ingredient
from users.models import User


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name')
    list_filter = ('author', 'name', 'tags')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('username', 'email')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
