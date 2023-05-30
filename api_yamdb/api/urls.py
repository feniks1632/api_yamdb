from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import CategoryViewSet, GenreViewSet, TitleViewSet, CommentsViewset, ReviewsViewset
from users.views import SignUpView, TokenView
from users.views import UsersView

router = DefaultRouter()
router.register('users', UsersView, basename='users')
router.register('genres', GenreViewSet, basename='genre')
router.register('categories', CategoryViewSet, basename='category')
router.register('titles', TitleViewSet, basename='title')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewset, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentsViewset, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
]

