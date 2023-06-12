import re

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


def username_validator(username):
    if username == 'me':
        raise ValidationError('"me" is not allowed as a username',
                              params={'username': username})
    if not re.match(r'^[\w.@+-]+$', username):
        raise ValidationError('This username is not allowed',
                              params={'username': username})


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    roles = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        default=''
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        default=''
    )
    username = models.CharField(
        verbose_name='Никнейм',
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    bio = models.TextField(
        null=True,
        verbose_name='Био',
        blank=True
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=25,
        default=USER,
        choices=roles
    )

    confirmation_code = models.CharField(max_length=10)

    def check_confirmation_code(self, confirmation_code):
        return self.confirmation_code == confirmation_code

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def __str__(self):
        return self.username
