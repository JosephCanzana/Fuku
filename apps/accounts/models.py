from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):

    # built in: username, password, email, is_superuser, last_login, date_joined, is_active, is_staff, groups, user_permissions
    email = models.EmailField(unique=True, blank=False)

    def __str__(self):
        return self.username
