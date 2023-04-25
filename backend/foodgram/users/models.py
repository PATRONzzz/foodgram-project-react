from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
