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

TABLES = {
    User: USERS,
    Category: CATEGORY,
    Genre: GENRE,
}


class Command(BaseCommand):
    help = 'Загружает данные из csv файлов в базу даных'

    def exist(self):
        pass

    # def load_genre_category_users(self):
    #     for model, csv_f in TABLES.items():
    #         with open(
    #             f'{PATH}{csv_f}',
    #             'r',
    #             encoding=UTF
    #         ) as csv_file:
    #             reader = DictReader(csv_file)
    #             model.objects.bulk_create(
    #                 model(**data) for data in reader
    #             )
    #     self.stdout.write(self.style.SUCCESS(
    #         f'{GENRE} {MESSAGE}'
    #         f'{CATEGORY} {MESSAGE}'
    #         f'{USERS} {MESSAGE}')
    #     )

    def load_genre(self):
        for row in DictReader(
                open(f'{PATH}{GENRE}', encoding=UTF)):
            Genre.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'])

        self.stdout.write(self.style.SUCCESS(
            f'{GENRE} {MESSAGE}')
        )

    def load_category(self):
        for row in DictReader(
                open(f'{PATH}{CATEGORY}', encoding=UTF)):
            Category.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'])

        self.stdout.write(self.style.SUCCESS(
            f'{CATEGORY} {MESSAGE}')
        )

    def load_title(self):
        for row in DictReader(
                open(f'{PATH}{TITLE}', encoding=UTF)):
            Title.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category']))

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
            User.objects.get_or_create(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )

        self.stdout.write(self.style.SUCCESS(
            f'{USERS} {MESSAGE}')
        )

    def load_review(self):
        for row in DictReader(
                open(f'{PATH}{REVIEW}', encoding=UTF)):
            Review.objects.get_or_create(
                id=row['id'],
                title=Title.objects.get(pk=row['title_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                score=row['score'],
                pub_date=row['pub_date'])

        self.stdout.write(self.style.SUCCESS(
            f'{REVIEW} {MESSAGE}')
        )

    def load_comments(self):
        for row in DictReader(
                open(f'{PATH}{COMMENTS}', encoding=UTF)):
            Comments.objects.get_or_create(
                id=row['id'],
                review=Review.objects.get(id=row['review_id']),
                text=row['text'],
                author=User.objects.get(id=row['author']),
                pub_date=row['pub_date'])

        self.stdout.write(self.style.SUCCESS(
            f'{REVIEW} {MESSAGE}')
        )

    def handle(self, *args, **options):
        try:
            # self.load_genre_category_users()
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
