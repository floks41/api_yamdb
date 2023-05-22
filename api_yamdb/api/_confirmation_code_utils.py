from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api_yamdb.settings import ADMIN_EMAIL
from users.models import User

EMAIL_SUBJECT_FOR_USER_CONFIRMATION_CODE = " Your confirmation code"


def set_and_send_user_confirmation_code(self, user: User) -> None:
    """Код подтверждения. Генерирует и отправляет по электронной почте.
    Генерирует, сохраняет в объекте пользователя и отправляет
    по электронной почте код подтверждения.
    """
    user.confirmation_code = default_token_generator.make_token(user)
    user.save()
    send_mail(subject=EMAIL_SUBJECT_FOR_USER_CONFIRMATION_CODE,
              message=user.confirmation_code,
              from_email=ADMIN_EMAIL,
              recipient_list=[user.email, ])
