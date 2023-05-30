from django.urls import include, path
from rest_framework import routers

from .views import (UsersView)

app_name = 'users'
router = routers.DefaultRouter()
router.register(r'api/v1/users', UsersView)
# router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentsViewSet,
#     basename='comments'
# )




