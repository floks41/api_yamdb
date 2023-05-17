from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comments, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comments
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для SAFE_METHODS к произведениям."""
    category = CategorySerializer(many=False, required=False)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и частичного изменения
     информации о произведении."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field="slug",
        many=True,
    )

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = request.user
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title, author=author
            ).exists():
                raise ValidationError(
                    'Вы не можете добавить более одного отзыва на произведение'
                )
        return data
