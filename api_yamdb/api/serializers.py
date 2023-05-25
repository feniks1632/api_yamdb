from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Review

User = get_user_model()


class TitleSerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    pass


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
