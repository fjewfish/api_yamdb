from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс пользователя."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    password = models.CharField(max_length=128, blank=True)
    email = models.EmailField(
        verbose_name='почта',
        unique=True,
        blank=False,
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='роль',
        max_length=16,
        choices=ROLES,
        default=USER,
    )
    confirmation_code = models.CharField(blank=True, max_length=24)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.username
