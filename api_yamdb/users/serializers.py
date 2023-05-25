import random
import re
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb import settings
from .models import User
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()


    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if len(email) > 254:
            raise serializers.ValidationError('Email address is too long.')
        
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError('Username contains invalid characters.')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email is already in use.')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username is already in use.')
        
        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        confirmation_code = random.randint(100000, 999999)

        # Сохраняем пользователя
        user = User.objects.create_user(email=email, username=username, confirmation_code=confirmation_code)

        #подтверждающий код на email пользователя
        send_mail(
            'Подтверждение регистрации',
            f'Ваш код подтверждения: {confirmation_code}',
            'from@example.com',
            [validated_data['email']],  # измененный параметр получателя письма
            fail_silently=False,
        )

        return user
    

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(User, username=username)
        print(user.username)
        if user is None:
            raise serializers.ValidationError('Invalid username',)
        if confirmation_code != user.confirmation_code:
            raise serializers.ValidationError('Invalid confirmation code')
        
        access = AccessToken.for_user(user)

        return {'token': str(access)}

    


    
