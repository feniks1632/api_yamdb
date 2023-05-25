import random
import re
from rest_framework import serializers
from .models import User
from django.core.mail import send_mail


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
        user = User.objects.create_user(**validated_data)

        send_mail(
        'Тема письма',
        'Текст письма.',
        'from@example.com', 
        ['to@example.com'],  
        fail_silently=False, 
) 

        return user

    
