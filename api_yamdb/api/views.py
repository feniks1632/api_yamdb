from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from reviews.models import Genre, Category, Title
from .serializers import GenreSerializer, CategorySerializer, TitleCreateSerializer, TitleSerializer
from .permissions import AdminOrReadOnly

class CreateListDeleteViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass

class GenreViewSet(CreateListDeleteViewset):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    paginator_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        genre = get_object_or_404(Genre, slug=kwargs)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(CreateListDeleteViewset):
    queryset =Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    paginator_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'

    def destroy(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TitleViewSet(viewsets.ModelViewSet):
    queryset =Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    paginator_class = PageNumberPagination
    filterset_fields = ('category', 'genre', 'name', 'year',)

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return TitleSerializer
        return TitleCreateSerializer


