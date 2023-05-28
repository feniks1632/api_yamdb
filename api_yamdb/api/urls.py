from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import CategoryViewSet, GenreViewSet, TitleViewSet, CommentsViewset, ReviewsViewset

router = DefaultRouter()
router.register('v1/genres', GenreViewSet, basename='genre')
router.register('v1/categories', CategoryViewSet, basename='category')
router.register('v1/titles', TitleViewSet, basename='title')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewset, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentsViewset, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]

