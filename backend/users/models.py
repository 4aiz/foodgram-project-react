import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def username_validator(username):
    if username == 'me':
        raise ValidationError('"me" is not allowed as a username',
                              params={'username': username})
    if not re.match(r'^[\w.@+-]+$', username):
        raise ValidationError('This username is not allowed',
                              params={'username': username})


class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'
    roles = (
        (ADMIN, 'admin'),
        (USER, 'user'),
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=25,
        default=USER,
        choices=roles
    )
    is_subscribed = models.BooleanField(
        default=False,
    )

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username
