from django.contrib.auth.models import AbstractUser
from django.db import models
from main.models import UserFollows


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    subscriptions = models.ManyToManyField("self", symmetrical=False, through=UserFollows, blank=True)
