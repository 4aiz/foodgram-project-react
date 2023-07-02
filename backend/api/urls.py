from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SetPasswordViewSet, UserCreateViewSet

from .views import IngredientViewSet, RecipeViewSet, TagsViewSet

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
# router.register(
#     r'^recipes/(?P<recipe_id>\d+)/favorite', RecipeViewSet, basename='favorite'
# )
# router.register(
#     r'^users/(?P<user_id>\d+)/subscribe',
#     UserCreateViewSet,
#     basename='subscribe'
# )
# router.register(
#     r'users/subscriptions',
#     UserCreateViewSet,
#     basename='subscriptions'
# )
router.register(
    r'users/set_password',
    SetPasswordViewSet,
    basename='set_password'
)
router.register(r'users', UserCreateViewSet, basename='users')
# router.register(
#     r'^recipes/(?P<recipe_id>\d+)/shopping_cart',
#     RecipeViewSet,
#     basename='shopping_cart'
# )

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
