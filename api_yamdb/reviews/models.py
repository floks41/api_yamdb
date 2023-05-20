from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(max_length=255, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, db_index=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=255,
                            verbose_name='Название произведения')
    year = models.IntegerField(
        verbose_name='Год выпуска', validators=[MinValueValidator(
            0, message='Год выпуска не может быть меньше 0'
        ), MaxValueValidator(
            datetime.now().year,
            message='Год выпуска не может быть больше текущего')])
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='categories', verbose_name='Категория')
    genre = models.ManyToManyField(Genre, related_name='titles',
                                   verbose_name='Жанры')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Название произведения'
        verbose_name_plural = 'Названия произведений'
        ordering = ('-year',)


class Review(models.Model):
    """Модель отзывов на произведения."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              verbose_name='Название произведения')
    text = models.TextField(max_length=1000, verbose_name='Текст ревью')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='review',
                               verbose_name='Автор ревью')
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        help_text='Укажите рейтинг',
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 0'),
            MaxValueValidator(10, message='Оценка не может быть больше 10')])
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Модель комментариев к отзывам."""
    review = models.ForeignKey(Review, unique=False, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Комментарий к отзыву')
    text = models.TextField(max_length=1000, verbose_name='Текст комментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор комментария')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
