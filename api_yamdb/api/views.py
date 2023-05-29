from rest_framework import viewsets, filters, status
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from reviews.models import Genre, Category, Title, Review
from users.perrmissions import IsAdminOrReadOnly
from .pagination import CommonPagination
from .serializers import GenreSerializer, CategorySerializer, TitleCreateSerializer, TitleSerializer, CommentSerializer, ReviewSerializer
from .permissions import AdminOrReadOnly

class CreateListDeleteViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass

class GenreViewSet(CreateListDeleteViewset):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = CommonPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    

    def destroy(self, request, *args, **kwargs):
        genre = get_object_or_404(Genre, slug=kwargs['pk'])
        if request.user.is_admin:
            self.perform_destroy(genre)
            return Response(status=status.HTTP_204_NO_CONTENT)
    def perform_destroy(self, genre):
        genre.delete()
        


class CategoryViewSet(CreateListDeleteViewset):
    queryset =Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = CommonPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    

    def destroy(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs['pk'])
        if request.user.is_admin:
            self.perform_destroy(category)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, category):
        category.delete()

class TitleViewSet(viewsets.ModelViewSet):
    queryset =Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CommonPagination
    filterset_fields = ('category', 'genre', 'name', 'year',)

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return TitleSerializer
        return TitleCreateSerializer
    

class CommentsViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer()
    permission_classes = (AdminOrReadOnly,)
    pagination_class = CommonPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class ReviewsViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.OrderingFilter,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


