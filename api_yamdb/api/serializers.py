import re

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User

USERNAME_PATTERN = r'^[\w.@+-]+\Z'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comments
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для SAFE_METHODS к произведениям."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и частичного изменения
     информации о произведении."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'


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
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id'))
        author = self.context.get('request').user
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(
                    title=title, author=author
            ).exists():
                raise ValidationError(
                    'Вы не можете добавить более одного отзыва на произведение'
                )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User, основной."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserUsernameValidationSerializer(UserSerializer):
    """Абстрактный сериализатор для модели User
    c валидатором для поля username.
    """
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Пользователь не может иметь username me.')

        if not re.compile(USERNAME_PATTERN).match(value):
            raise serializers.ValidationError(
                'Username. 150 символов или меньше. '
                'Буквы, цифры и @/./+/-/_ only.')

        return value


class UserMePatchSerializer(UserUsernameValidationSerializer):
    """Сериализатор модели User для эндпоинта users/me/ метода PATCH."""
    username = serializers.CharField(required=False, max_length=150)
    email = serializers.EmailField(required=False, max_length=254)

    class Meta(UserUsernameValidationSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(UserUsernameValidationSerializer):
    """Сериализатор модели User для эндпоинта auth/signup/.
    Регистрация пользователя.
    """
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    def __init__(self, data, instance=None, **kwargs):
        """Дополнительно подбирает объект из модели, если такой есть.
        Сохраняет в self.instance. При отсутствии объекта
        исключений не выдает.
        """
        super().__init__(instance, data, **kwargs)

        username = self.initial_data.get('username')
        if (username and self.Meta.model.objects.filter(
                username=username).exists()):
            self.instance = self.Meta.model.objects.get(username=username)

    def validate_email(self, value):
        if self.instance:
            if value != self.instance.email:
                raise serializers.ValidationError('Неверный email.')
        else:
            if self.Meta.model.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    'Пользователь с указанным email уже зарегистрирован.')
        return value

    class Meta(UserUsernameValidationSerializer.Meta):
        fields = ('username', 'email')


class AuthGetTokenSerializer(SignUpSerializer):
    """Сериализатор модели User для эндпоинта auth/token/. Получение токена."""
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        return str(AccessToken.for_user(obj).token)

    def validate_confirmation_code(self, value):
        if self.instance and value != self.instance.confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения.')
        return value

    def validate_username(self, value):
        if not self.instance:
            raise NotFound('Неверное имя пользователя.')
        return super().validate_username(value)

    class Meta(SignUpSerializer.Meta):
        write_only_fields = ('username', 'confirmation_code')
        fields = ('username', 'confirmation_code', 'token')
