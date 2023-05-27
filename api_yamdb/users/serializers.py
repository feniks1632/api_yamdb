from http import HTTPStatus
import random
import re
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api_yamdb import settings
from .models import User, ROLE_CHOISES
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username')
        
    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if len(email) > 254:
            raise serializers.ValidationError('Email address is too long.')
        
        if len(username) > 150:
            raise serializers.ValidationError('Email address is too long.')
        
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError('Username contains invalid characters.')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email is already in use.')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username is already in use.')
        
        if username == 'me':
            raise serializers.ValidationError('Invalid username')

        return data
        

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        confirmation_code = random.randint(100000, 999999)

        # Сохраняем пользователя
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(email=email, username=username, confirmation_code=confirmation_code)
            send_mail(
            'Подтверждение регистрации',
            f'Ваш код подтверждения: {confirmation_code}',
            'from@example.com',
            [validated_data['email']],
            fail_silently=False,
        )

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
            raise serializers.ValidationError('Invalid username',)
        if confirmation_code != user.confirmation_code:
            raise serializers.ValidationError('Invalid confirmation code')
        
        access = AccessToken.for_user(user)

        return {'token': str(access)}
    

class UsersSerializer(serializers.ModelSerializer):
     email = serializers.EmailField(required=True)
     username = serializers.CharField(required=True)
     first_name = serializers.CharField(required=False)
     last_name = serializers.CharField(required=False)
     bio = serializers.CharField(required=False)
     role = serializers.ChoiceField(required=False, choices=ROLE_CHOISES, default="user",)      

     class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

     def validate(self, data):
        email = data.get('email')
        username = str(data.get('username'))
        first_name = data.get('first_name')
        last_name = data.get('last_name')



        if email and len(email) > 254:
            raise serializers.ValidationError('Email address is too long.')
        
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError('Username contains invalid characters.')
        
        if username and len(username) > 150:
            raise serializers.ValidationError('Email address is too long.')
        
        if first_name and len(first_name) > 150:
            raise serializers.ValidationError('Email address is too long.')
        
        if last_name and len(last_name) > 150:
            raise serializers.ValidationError('Email address is too long.')
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email is already in use.')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('This username is already in use.')
        
        return data


     def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        first_name= str(validated_data.get('first_name'))
        last_name= str(validated_data.get('last_name'))
        bio= str(validated_data.get('bio'))
        role = str(validated_data.get('role'))
        confirmation_code = random.randint(100000, 999999)

        user = User.objects.create_user(email=email, username=username, confirmation_code=confirmation_code, first_name=first_name, last_name=last_name, bio=bio, role=role )
            
        return user 
     
     def partial_update(self, validate_date):
         role = validate_date('role')
         if role not in ROLE_CHOISES:
            return HTTPStatus.BAD_REQUEST
             


    


    
