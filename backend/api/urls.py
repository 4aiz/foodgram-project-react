from django.urls import path, include
from rest_framework.authtoken import views as v
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


# from .views import ()
from users.views import UserViewSet

router = DefaultRouter()

# router.register(r'recipes', TitlesViewSet, basename='recipes')
# router.register(r'tags', GenresViewSet, basename='tags')
# router.register(r'ingredients', CategoriesViewSet, basename='ingredients')
# router.register(
#     r'^recipes/(?P<title_id>\d+)/reviews', ReviewViewset, basename='reviews'
# )
# router.register(
#     r'^recipes/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewset,
#     basename='comments'
# )

app_name = 'api'

urlpatterns = [
    path('users/me', UserViewSet),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
