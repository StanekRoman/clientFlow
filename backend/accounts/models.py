
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # autopep8: off
    objects: ClassVar[CustomUserManager] = CustomUserManager() # pyright: ignore[reportIncompatibleVariableOverride]
    # autopep8: on

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                name='unique_user_email_ci'
            ),
        ]

    def __str__(self):
        return self.email
