import logging
import sys
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

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(FORMATTER)
    logger.addHandler(handler)
    return logger


logger = get_logger('load_data')


class Command(BaseCommand):

    def exist(self):
        pass

    def load_genre(self):
        for row in DictReader(
                open(f'{PATH}{GENRE}', encoding=UTF)):
            Genre.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'])

        logger.info(f'{GENRE} {MESSAGE}')

    def load_category(self):
        for row in DictReader(
                open(f'{PATH}{CATEGORY}', encoding=UTF)):
            Category.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'])

        logger.info(f'{CATEGORY} {MESSAGE}')

    def load_title(self):
        for row in DictReader(
                open(f'{PATH}{TITLE}', encoding=UTF)):
            Title.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=Category.objects.get(id=row['category']))

        logger.info(f'{TITLE} {MESSAGE}')

    def load_genre_title(self):
        for row in DictReader(
                open(f'{PATH}{GENRE_TITLE}')):
            Title.objects.get(
                id=row['title_id']).load_genre.add(row['genre_id'])

        logger.info(f'{GENRE_TITLE} {MESSAGE}')

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

        logger.info(f'{USERS} {MESSAGE}')

    def load_review(self):
        try:
            for row in DictReader(
                    open(f'{PATH}{REVIEW}', encoding=UTF)):
                Review.objects.get_or_create(
                    id=row['id'],
                    title=Title.objects.get(pk=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'])

        except IntegrityError as err:
            logger.error(err)
            exit()

        logger.info(f'{REVIEW} {MESSAGE}')

    def load_comments(self):
        try:
            for row in DictReader(
                    open(f'{PATH}{COMMENTS}', encoding=UTF)):
                Comments.objects.get_or_create(
                    id=row['id'],
                    review=Review.objects.get(id=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date']
                )

        except IntegrityError as err:
            logger.error(err)
            exit()

        logger.info(f'{COMMENTS} {MESSAGE}')

    def handle(self, *args, **options):
        self.load_category()
        self.load_genre()
        self.load_title()
        self.load_genre_title()
        self.load_users()
        self.load_review()
        self.load_comments()
