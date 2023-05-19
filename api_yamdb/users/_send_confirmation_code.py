from django.core.mail import send_mail
from users.models import User

from api_yamdb.settings import (ADMIN_EMAIL,
                                EMAIL_SUBJECT_USER_CONFIRMATION_CODE)


def send_user_confirmation_code(self, user: User):
    """Отправляет код подтверждения на адрес электронной почты пользователя."""

    send_mail(subject=EMAIL_SUBJECT_USER_CONFIRMATION_CODE,
              message=user.confirmation_code,
              from_email=ADMIN_EMAIL,
              recipient_list=[user.email, ])
    