from django.db import models

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
