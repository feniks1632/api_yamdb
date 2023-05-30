from rest_framework import routers

from .views import (UsersView)

app_name = 'users'
router = routers.DefaultRouter()
router.register(r'api/v1/users', UsersView)
