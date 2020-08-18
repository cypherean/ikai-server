from django.db import models
from django.contrib.auth.models import User


class UserKeys(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    publickey = models.CharField(max_length=2000)
