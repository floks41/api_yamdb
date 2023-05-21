from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.utils.translation import gettext_lazy as _

USER_ROLE = 'user'
MODERATOR_ROLE = 'moderator'
ADMIN_ROLE = 'admin'
STAFF_USER_ROLES = (MODERATOR_ROLE, ADMIN_ROLE)

USER_ROLES = (
    (USER_ROLE, 'пользователь'),
    (MODERATOR_ROLE, 'модератор'),
    (ADMIN_ROLE, 'администратор')
)


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=254,
        error_messages={
            'unique': _("Пользователь с указанным email уже существует."),
        })
    role = models.CharField(
        max_length=255,
        choices=USER_ROLES,
        default=USER_ROLE,
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

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN_ROLE

    @property
    def is_project_staff(self):
        return self.is_superuser or self.role in STAFF_USER_ROLES

    class Meta:
        constraints = [
            CheckConstraint(
                check=~Q(username='me'),
                name='username_not_me'
            ),
            UniqueConstraint(
                fields=['username', 'email', ],
                name='Unique_email_for_each_username',
            )
        ]
        ordering = ['id']
