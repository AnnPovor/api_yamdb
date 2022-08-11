from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    role = models.CharField(verbose_name='Роль',
                            max_length=50,
                            choices=ROLE_CHOICES,
                            blank=True,
                            null=True,
                            default=USER
                            )

    username = models.CharField(verbose_name='Имя пользователя',
                                max_length=150,
                                unique=True,

                                )
    email = models.EmailField(verbose_name='Адрес электронной почты',
                              unique=True)

    bio = models.CharField(max_length=100,
                           verbose_name='О себе')

    confirmation_code = models.CharField(max_length=256, default=uuid.uuid4)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
