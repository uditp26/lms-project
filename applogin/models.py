from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (0, 'Superuser'),
        (1, 'Student'),
        (2, 'Teacher'),
        (3, 'Principal'),
        (4, 'Admin'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=0)