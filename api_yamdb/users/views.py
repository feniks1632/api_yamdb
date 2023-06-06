from django.shortcuts import get_object_or_404

from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action

from .models import User
from .perrmissions import IsAdmin
from .serializers import SignUpSerializer, TokenSerializer, UsersSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user:
            return Response(request.data, status=status.HTTP_200_OK)

        response_data = {
            'email': user.email,
            'username': user.username,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class TokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class UsersView(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdmin]
    filter_backends = [SearchFilter]
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def partial_update(self, request, *args, **kwargs):
        username = self.kwargs[self.lookup_field]
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        request_data = request.data.copy()
        if 'role' in request.data:
            request_data['role'] = request.user.role
        serializer = self.get_serializer(user, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
