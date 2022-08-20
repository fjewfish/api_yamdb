from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Title, Genre, Category, Review

from .filters import TitleFilter
from .utils import send_confirmation_code
from .permissions import (IsAdminOrReadOnly, IsOwnerAdminModeratorOrReadOnly,
                          IsAdminRole)
from .serializers import (CategorySerializer, GenreSerializer,
                          CommentSerializer,
                          ReviewSerializer, TitleSerializer,
                          TitleCreateSerializer,
                          UserSerializer, UserMeSerializer,
                          ConfirmationCodeSerializer,
                          CustomTokenObtainPairSerializer,
                          )

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Viewset для модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminRole,)
    lookup_field = "username"

    @action(
        detail=False,
        serializer_class=UserMeSerializer,
        permission_classes=(IsAuthenticated,),
        methods=['get', 'patch'],
    )
    def me(self, request):
        """GET, PATCH запросы на users/me/."""
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class SignupConfirmationCodeSend(APIView):
    """
    Создает нового пользователя.
    Отсылает confirmation_code по email и записывает его в модель User.
    """
    permission_classes = (AllowAny,)

    def _generate_and_send_token(self, user):
        user.confirmation_code = default_token_generator.make_token(user)
        send_confirmation_code(user.email, user.confirmation_code)
        user.save()

    def post(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            User, username=serializer.data['username']
        )
        self._generate_and_send_token(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Возвращает JSON web token."""
    serializer_class = CustomTokenObtainPairSerializer


class ListCreateDestroyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerAdminModeratorOrReadOnly, ]

    def get_queryset(self):
        title_pk = self.kwargs.get('title_pk')
        title = get_object_or_404(Title, id=title_pk)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_pk'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerAdminModeratorOrReadOnly, ]

    def get_queryset(self):
        review_pk = self.kwargs.get('review_pk')
        title = get_object_or_404(Title, reviews=review_pk)
        review = get_object_or_404(Review, id=review_pk, title=title)
        return review.comments.all()

    def perform_create(self, serializer):
        review_pk = self.kwargs.get('review_pk')
        title = get_object_or_404(Title, reviews=review_pk)
        review = get_object_or_404(Review, pk=review_pk, title=title)
        serializer.save(author=self.request.user, review=review)
