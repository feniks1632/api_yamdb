from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register('v1/genres', GenreViewSet, basename='genre')
router.register('v1/categories', CategoryViewSet, basename='category')
router.register('v1/titles', TitleViewSet, basename='title')

urlpatterns = [
    path('', include(router.urls)),
]

