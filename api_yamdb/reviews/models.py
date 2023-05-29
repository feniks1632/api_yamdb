from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint

User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True,)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(Category, related_name='titles', on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.name

class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='rewiews',
        verbose_name='Произведение',
        help_text='Выберите произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rewiews',
        verbose_name='Автор',
        help_text='Выберите автора'
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Напишите свой отзыв'
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Значения от 1 до 10'),
            MaxValueValidator(10, 'Значения от 1 до 10')
        ],
        verbose_name='Оценка',
        help_text='Поставьте оценку'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв',
        verbose_name_plural = 'Отзывы',
        constraints = (
            CheckConstraint(
                check=Q(score__lte=10),
                name='score_lte_10'),
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_reviewing'
            )
        )

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии',
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:25]