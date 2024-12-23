from django.contrib.auth.models import User
from django.db import models


class TelegramProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.BigIntegerField(unique=True)
    telegram_username = models.CharField(max_length=150, blank=True, null=True)
    auth_token = models.CharField(max_length=255, unique=True)