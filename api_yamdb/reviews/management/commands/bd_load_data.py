from django.core.management import BaseCommand

from csv import DictReader
import codecs

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        with codecs.open(
            'static/data/category.csv',
                'r', encoding='utf-8') as f:
            for row in DictReader(f):
                category = Category(
                    name=row['name'],
                    id=row['id'],
                    slug=row['slug']
                )
                category.append(category)
                Category.objects.bulk_create(Category)

        with codecs.open('static/data/genre.csv', 'r', encoding='utf-8') as f:
            for row in DictReader(f):
                genre = Genre(name=row['name'], id=row['id'], slug=row['slug'])
                genre.append(genre)
                Genre.objects.bulk_create(Genre)

        with codecs.open('static/data/titles.csv', 'r', encoding='utf-8') as f:
            for row in DictReader(f):
                title = Title(
                    name=row['name'],
                    id=row['id'],
                    year=row['year'],
                    category=Category.objects.get(pk=row['category'])
                )
                title.append(title)
                Title.objects.bulk_create(Title)

        with codecs.open('static/data/users.csv', 'r', encoding='utf-8') as f:
            for row in DictReader(f):
                user = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                user.append(user)
                User.objects.bulk_create(User)

        with codecs.open('static/data/review.csv', 'r', encoding='utf-8') as f:
            for row in DictReader(f):
                review = Review(
                    id=row['id'],
                    title=Title.objects.get(pk=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                review.append(review)
                Review.objects.bulk_create(Review)

        with codecs.open(
                'static/data/comments.csv', 'r', encoding='utf-8') as f:
            for row in DictReader(f):
                comment = Comment(
                    id=row['id'],
                    review=Review.objects.get(pk=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    pub_date=row['pub_date']
                )
                comment.append(comment)
                Comment.objects.bulk_create(Comment)
