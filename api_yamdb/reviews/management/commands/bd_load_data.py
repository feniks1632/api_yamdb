import pandas as pd

from django.core.management import BaseCommand
from reviews.models import (
    Category, Comment, Genre, GenreTitle, Review, Title,
)

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = pd.read_csv('static/data/genre.csv')
        row_iter = data.iterrows()
        genres = [
            Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            for index, row in row_iter
        ]
        Genre.objects.bulk_create(genres,)

        data = pd.read_csv('static/data/category.csv')
        row_iter = data.iterrows()
        categories = [
            Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            for index, row in row_iter
        ]
        Category.objects.bulk_create(categories,)

        data = pd.read_csv('static/data/titles.csv')
        row_iter = data.iterrows()
        titles = [
            Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(pk=row['category']),
            )
            for index, row in row_iter
        ]
        Title.objects.bulk_create(titles,)

        data = pd.read_csv('static/data/genre_title.csv')
        row_iter = data.iterrows()
        genres_titles = [
            GenreTitle(
                id=row['id'],
                title_id=Title.objects.get(pk=row['title_id']),
                genre_id=Genre.objects.get(pk=row['genre_id']),
            )
            for index, row in row_iter
        ]
        GenreTitle.objects.bulk_create(genres_titles,)

        data = pd.read_csv('static/data/users.csv')
        row_iter = data.iterrows()
        users = [
            User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=['first_name'],
                last_name=['last_name'],
            )
            for index, row in row_iter
        ]
        User.objects.bulk_create(users,)

        data = pd.read_csv('static/data/review.csv')
        row_iter = data.iterrows()
        reviews = [
            Review(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                score=row['score'],
                pub_date=row['pub_date'],
            )
            for index, row in row_iter
        ]
        Review.objects.bulk_create(reviews,)

        data = pd.read_csv('static/data/comments.csv')
        row_iter = data.iterrows()
        comments = [
            Comment(
                id=row['id'],
                review=Review.objects.get(pk=row['review_id']),
                text=row['text'],
                author=User.objects.get(pk=row['author']),
                pub_date=row['pub_date'],
            )
            for index, row in row_iter
        ]
        Comment.objects.bulk_create(comments,)
