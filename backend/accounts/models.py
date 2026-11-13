
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  # pyright: ignore[reportAssignmentType]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('email'),
                name='unique_user_email_ci'
            ),
        ]

    def __str__(self):
        return self.email
