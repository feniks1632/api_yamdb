from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404

from reviews.models import Review
from .pagination import CommonPagination
from .permissions import IsOwner
from .serializers import CommentSerializer, ReviewSerializer


class CommentsViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer()
    permission_classes = (IsOwner,)
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
    permission_classes = (IsOwner,)
    filter_backends = (filters.OrderingFilter,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CategoriesViewSet(viewsets.ModelViewSet):
    pass


class TitlesViewSet(viewsets.ModelViewSet):
    pass


class GenresViewSet(viewsets.ModelViewSet):
    pass

