from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Genre, Category,Title, Comment, Review
from datetime import datetime
from django.shortcuts import get_object_or_404

User = get_user_model()

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)
    rating = serializers.FloatField(
        source = 'reviews__score__avg',
        read_only=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField (
        slug_field = 'slug',
        many=True,
        queryset=Genre.objects.all(),
        required=True,
        )
    category = SlugRelatedField (
        slug_field = 'slug',
        many=True,
        queryset=Category.objects.all(),
        required=True,
        )
    

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)
        model = Title

    def validate_year(self, value):
        year = datetime.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выпуска произведения')
        return value
    
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
    slug_field='username',
    read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    rating = serializers.IntegerField(
        min_value=1,
        max_value=10
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'rating', 'pub_date',)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = get_object_or_404(
            Title,
            id=self.context['request'].parser_context['kwargs']['title_id']
        )
        if Review.objects.filter(
            author=self.context['request'].user,
            title=title
        ).exists():
            raise serializers.ValidationError('Отзыв уже оставлен')
        return data
