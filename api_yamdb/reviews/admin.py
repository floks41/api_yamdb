from django.contrib import admin

from .models import Category, Comments, Genre, Review, Title


@admin.register(Title)
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
    list_display = ('text',  'author')


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
