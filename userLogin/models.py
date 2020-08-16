from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, username, public_key, password):
        user = self.model(
            username=username,
            public_key=public_key,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, public_key, password):
        user = self.create_user(
            username=username,
            password=password,
            public_key=public_key
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, public_key, password):
        user = self.create_user(
            username=username,
            password=password,
            public_key=public_key
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    public_key = models.CharField(max_length=2000)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['public_key']
    objects = UserManager()
