from csv import DictReader

from django.core.management import BaseCommand
from django.db.utils import IntegrityError

from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User

PATH = 'static/data/'
GENRE = 'genre.csv'
CATEGORY = 'category.csv'
TITLE = 'titles.csv'
GENRE_TITLE = 'genre_title.csv'
USERS = 'users.csv'
REVIEW = 'review.csv'
COMMENTS = 'comments.csv'
MESSAGE = 'был успешно загружен в базу данных.'
UTF = 'UTF-8'


class Command(BaseCommand):
    help = 'Загружает данные из csv файлов в базу данных'

    def load_genre(self):
        for row in DictReader(
                open(f'{PATH}{GENRE}', encoding=UTF)):
            Genre.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS(
            f'{GENRE} {MESSAGE}')
        )

    def load_category(self):
        for row in DictReader(
                open(f'{PATH}{CATEGORY}', encoding=UTF)):
            Category.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS(
            f'{CATEGORY} {MESSAGE}')
        )

    def load_title(self):
        for row in DictReader(
                open(f'{PATH}{TITLE}', encoding=UTF)):
            Title.objects.get_or_create(
                category=Category.objects.get(id=row.pop('category')), **row)

        self.stdout.write(self.style.SUCCESS(
            f'{TITLE} {MESSAGE}')
        )

    def load_genre_title(self):
        for row in DictReader(
                open(f'{PATH}{GENRE_TITLE}')):
            Title.objects.get(
                id=row['title_id']).genre.add(row['genre_id'])

        self.stdout.write(self.style.SUCCESS(
            f'{GENRE_TITLE} {MESSAGE}')
        )

    def load_users(self):
        for row in DictReader(
                open(f'{PATH}{USERS}', encoding=UTF)):
            User.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS(
            f'{USERS} {MESSAGE}')
        )

    def load_review(self):
        for row in DictReader(
                open(f'{PATH}{REVIEW}', encoding=UTF)):
            Review.objects.get_or_create(
                title=Title.objects.get(pk=row.pop('title_id')),
                author=User.objects.get(id=row.pop('author')),
                **row)

        self.stdout.write(self.style.SUCCESS(
            f'{REVIEW} {MESSAGE}')
        )

    def load_comments(self):
        for row in DictReader(
                open(f'{PATH}{COMMENTS}', encoding=UTF)):
            Comments.objects.get_or_create(
                review=Review.objects.get(id=row.pop('review_id')),
                author=User.objects.get(id=row.pop('author')),
                **row)

        self.stdout.write(self.style.SUCCESS(
            f'{COMMENTS} {MESSAGE}')
        )

    def handle(self, *args, **options):
        try:
            self.load_category()
            self.load_genre()
            self.load_title()
            self.load_genre_title()
            self.load_users()
            self.load_review()
            self.load_comments()

        except IntegrityError as err:
            self.stdout.write(self.style.ERROR(
                f'ERROR - {err}')
            )
            exit()
