from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets

ROLE_CHOISES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):

    username = models.CharField(
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        max_length=150
    )
    last_name = models.CharField(
        max_length=150
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        choices=ROLE_CHOISES,
        max_length=20,
        default='user'
    )
    confirmation_code = models.CharField(max_length=6)
