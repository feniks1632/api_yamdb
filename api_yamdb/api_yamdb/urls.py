from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from users.views import SignUpView, TokenView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('api/v1/auth/token/', TokenView.as_view(), name='auth_token'),
    path('', include('users.urls')),
    
]