from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models import CheckConstraint, Q


USER_ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор')
)


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=254,
        error_messages={
            'unique': _("A user with that email address already exists."),
        })
    role = models.CharField(
        max_length=255,
        choices=USER_ROLES,
        default=USER_ROLES[0][0],
        verbose_name='Категория пользователя')

    bio = models.CharField(
        max_length=255,
        verbose_name='Описание пользователя', blank=True,
        null=True)

    confirmation_code = models.CharField(
        max_length=255,
        verbose_name='Действующий код подтверждения',
        blank=True,
        null=True)

    def __str__(self):
        return self.username
    
    class Meta:
        constraints = [
            CheckConstraint(
                check=~Q(username='me'),
                name='username_not_me'
            )
        ]
        ordering = ['id']
