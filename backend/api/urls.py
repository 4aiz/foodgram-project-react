from django.urls import path, include
from rest_framework.authtoken import views as v
from rest_framework.routers import DefaultRouter

from .views import (TitlesViewSet,
                    GenresViewSet,
                    CategoriesViewSet,
                    ReviewViewset,
                    CommentViewset)
from users import views

routerv1 = DefaultRouter()
routerv1.register(r'recipe', TitlesViewSet, basename='titles')
routerv1.register(r'', GenresViewSet, basename='genres')
routerv1.register(r'categories', CategoriesViewSet, basename='categories')
routerv1.register(
    r'^titles/(?P<title_id>\d+)/reviews', ReviewViewset, basename='reviews'
)
routerv1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewset,
    basename='comments'
)

app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', views.SignupView.as_view()),
    path('v1/auth/token/', views.TokenView.as_view()),
    path('v1/users/', views.ProfileManage.as_view()),
    path('v1/users/<str:username>/', views.ProfileActions.as_view()),
    path('v1/api-token-auth/', v.obtain_auth_token),
    path('v1/', include(routerv1.urls)),
]
