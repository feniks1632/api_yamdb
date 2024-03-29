import random
import re

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db.models import Q

from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from .models import Role, User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs = {
            'username': {
                'validators': []
            },
            'email': {
                'validators': []
            }
        }

    def validate(self, data):
        email = data.get('email').lower()
        username = data.get('username').lower()

        if len(email) > 254:
            raise serializers.ValidationError('Email слишком длинный.')

        if len(username) > 150:
            raise serializers.ValidationError('Username слишком длинный.')

        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError('Недопустимые символы.')

        if username == 'me':
            raise serializers.ValidationError('Недопустимый username')

        if (User.objects.filter(
            Q(email=email) | Q(username=username)).exclude(
                email=email, username=username).exists()):
            raise serializers.ValidationError('Такой пользователь '
                                              'уже существует.')

        return super().validate(data)

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        code = random.randint(100000, 999999)

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(email=email, username=username,
                                            confirmation_code=code)
            send_mail('Подтверждение регистрации',
                      f'Ваш код подтверждения: {code}',
                      'from@example.com',
                      [validated_data['email']],
                      fail_silently=False)

            return user

        return User.objects.filter(username=username, email=email)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(User, username=username)
        if user is None:
            raise serializers.ValidationError('Неправильный пользователь',)
        if confirmation_code != user.confirmation_code:
            raise serializers.ValidationError('Неправильный код подтверждения')

        access = AccessToken.for_user(user)

        return {'token': str(access)}


class UsersSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    role = serializers.ChoiceField(required=False,
                                   choices=Role.choices,
                                   default=Role.user,)

    class Meta:
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        model = User
        extra_kwargs = {
            'username': {
                'validators': []
            },
            'email': {
                'validators': []
            }
        }

    def validate(self, data):
        email = data.get('email')
        username = str(data.get('username'))
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if email and len(email) > 254:
            raise serializers.ValidationError('Email слишком длинный.')

        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError('Недопустимые символы.')

        if username and len(username) > 150:
            raise serializers.ValidationError(
                'Username слишком длинный'
            )

        if first_name and len(first_name) > 150:
            raise serializers.ValidationError('Имя слишком длинное')

        if last_name and len(last_name) > 150:
            raise serializers.ValidationError('Фамилия слишком длинная')

        if (User.objects.filter(
            Q(email=email) | Q(username=username)).exclude(
                email=email, username=username).exists()):
            raise serializers.ValidationError('Такой пользователь '
                                              'уже существует.')

        return super().validate(data)

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        first_name = str(validated_data.get('first_name'))
        last_name = str(validated_data.get('last_name'))
        bio = str(validated_data.get('bio'))
        role = str(validated_data.get('role'))
        confirmation_code = random.randint(100000, 999999)

        user = User.objects.create_user(email=email,
                                        username=username,
                                        confirmation_code=confirmation_code,
                                        first_name=first_name,
                                        last_name=last_name,
                                        bio=bio,
                                        role=role)

        return user
