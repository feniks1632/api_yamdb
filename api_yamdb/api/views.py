from django.db.models import Count, Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from reviews.models import Category, Genre, Review, Title
from .filters import TitlesFilter
from .permissions import (
    IsAdminOrReadOnly,
    IsModeratorOrReadOnly,
    IsAuthorOrReadOnly,
)

from .serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleCreateSerializer,
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer
)


class CreateListDeleteViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class GenreViewSet(CreateListDeleteViewset):
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)

    def get_queryset(self):
        queryset = Genre.objects.filter(
            genretitle__title_id=self.kwargs.get('title_id'))
        return queryset

    def destroy(self, request, *args, **kwargs):
        genre = get_object_or_404(Genre, slug=kwargs['pk'])
        self.perform_destroy(genre)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, genre):
        genre.delete()


class CategoryViewSet(CreateListDeleteViewset):
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)

    def get_queryset(self):
        queryset = Category.objects.order_by('name').annotate(
            num_titles=Count('titles'),
        )
        return queryset

    def destroy(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs['pk'])
        self.perform_destroy(category)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, category):
        category.delete()


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_queryset(self):
        queryset = Title.objects.order_by('name').annotate(
            avg_rating=Avg('rewiews__score')
        )
        return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleCreateSerializer


class CommentsViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsModeratorOrReadOnly | IsAuthorOrReadOnly | IsAdminOrReadOnly]

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)


class ReviewsViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsModeratorOrReadOnly | IsAuthorOrReadOnly | IsAdminOrReadOnly]
    filter_backends = (filters.OrderingFilter,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        title = self.get_title()
        return title.rewiews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)

    def post(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)
