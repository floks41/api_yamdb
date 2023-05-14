from django.contrib import admin
from .models import Category, Genre, Titles, Review, Comments


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score', 'pub_date')


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
