from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    user = 'user', 'Пользователь'
    moderator = 'moderator', 'Модератор'
    admin = 'admin', 'Администратор'

    def __str__(self):
        return self.name


class User(AbstractUser):

    username = models.CharField(
        'Польователь',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'Электронная почта пользователя',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя пользователя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=150
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль пользователя',
        choices=Role.choices,
        max_length=20,
        default=Role.user
    )
    confirmation_code = models.CharField(
        'Поле с кодом подтверждения',
        max_length=6
    )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return f'{self.username}'

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
 

