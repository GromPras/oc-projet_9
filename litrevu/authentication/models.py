from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User Model to anticipate potential future modifications"""

    pass
