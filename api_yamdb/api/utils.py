from django.core.mail import send_mail

from api_yamdb.settings import DEFAULT_FROM_EMAIL


def send_confirmation_code(email, confirmation_code):
    """Функция для отправки email"""
    send_mail(
        'confirmation_code for registration',
        f'Check out your confirmation_code: {confirmation_code}',
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
