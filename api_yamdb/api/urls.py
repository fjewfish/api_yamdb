from django.urls import include, path
from rest_framework import routers
from .views import (CategoryViewSet, GenreViewSet, CommentViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    SignupConfirmationCodeSend,
                    CustomTokenObtainPairView)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet,
                basename='categories')
router.register(r'genres', GenreViewSet,
                basename='genres')
router.register(r'titles', TitleViewSet,
                basename='titles')
router.register(r'titles/(?P<title_pk>\d+)/reviews',
                ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_pk>\d+)/reviews/(?P<review_pk>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', SignupConfirmationCodeSend.as_view()),
    path('v1/auth/token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/', include(router.urls)),
]
