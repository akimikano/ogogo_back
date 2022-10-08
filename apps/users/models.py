from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    USER_TYPES = (
        ('worker', 'Работник'),
        ('client', 'Клиент')
    )

    type = models.CharField('Тип', max_length=6, choices=USER_TYPES)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


