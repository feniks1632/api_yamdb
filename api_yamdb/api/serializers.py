from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Genre, Category,Title
from datetime import datetime


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
