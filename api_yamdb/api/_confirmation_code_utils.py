from django.core.mail import send_mail
# from django.utils.crypto import get_random_string
from users.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator

from api_yamdb.settings import ADMIN_EMAIL

EMAIL_SUBJECT_FOR_USER_CONFIRMATION_CODE = " Your confirmation code"
# CONFIRMATION_CODE_LENGTH = 10
# CONFIRMATION_CODE_ALLOWED_CHARS = ('abcdefghjkmnpqrstuvwxyz'
#                                    'ABCDEFGHJKLMNPQRSTUVWXYZ'
#                                    '23456789')


def send_user_confirmation_code(self, user: User) -> None:
    """Отправляет код подтверждения на адрес электронной почты пользователя."""

    send_mail(subject=EMAIL_SUBJECT_FOR_USER_CONFIRMATION_CODE,
              message=user.confirmation_code,
              from_email=ADMIN_EMAIL,
              recipient_list=[user.email, ])


def generate_confirmation_code(self, user: User) -> str:
    """Генерирует и возвращает код подтверждения."""
    return token_generator.make_token(user)
    # return get_random_string(CONFIRMATION_CODE_LENGTH,
    #                          CONFIRMATION_CODE_ALLOWED_CHARS)


def set_and_send_confirmation_code(self, user: User) -> None:
    """Генерирует и сохраняет и отправляет по электронной почте 
    код подтверждения.
    """
    user.confirmation_code = token_generator.make_token(user)
    user.save()
    send_user_confirmation_code(self, user)

