from django.contrib.auth import get_user_model
from django.core.validators import (RegexValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from .utils import year_validator

slug_validator_regexp = RegexValidator(
    r'[-a-zA-Z0-9_]+$',
    'Only latin characters/numbers and underscore are available',
)
User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория произведения'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[slug_validator_regexp]
    )


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр произведения'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[slug_validator_regexp]
    )


class Title(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название произведения'
    )

    year = models.IntegerField(
        verbose_name='Год создания',
        validators=[year_validator]
    )

    rating = models.FloatField(
        verbose_name='Рейтинг произведения',
        default=None,
        null=True
    )

    description = models.CharField(
        max_length=1000,
        verbose_name='Описание произведения',
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения',
        related_name='titles',
        null=True
    )

    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения',
        related_name='titles',
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        verbose_name='ID произведения',
        on_delete=models.CASCADE,
    )
    text = models.CharField(max_length=255, verbose_name='Текст рецензии')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='ID рецензии',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.CharField(
        max_length=255,
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ['-id']
