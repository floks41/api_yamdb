from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from users.models import User

from api_yamdb.settings import ADMIN_EMAIL

EMAIL_SUBJECT_FOR_USER_CONFIRMATION_CODE = " Your confirmation code"
CONFIRMATION_CODE_LENGTH = 10
CONFIRMATION_CODE_ALLOWED_CHARS = ('abcdefghjkmnpqrstuvwxyz'
                                   'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                   '23456789')


def send_user_confirmation_code(self, user: User) -> None:
    """Отправляет код подтверждения на адрес электронной почты пользователя."""

    send_mail(subject=EMAIL_SUBJECT_FOR_USER_CONFIRMATION_CODE,
              message=user.confirmation_code,
              from_email=ADMIN_EMAIL,
              recipient_list=[user.email, ])


def generate_confirmation_code(self) -> str:
    """Генерирует и возвращает код подтверждения."""
    return get_random_string(CONFIRMATION_CODE_LENGTH,
                             CONFIRMATION_CODE_ALLOWED_CHARS)
