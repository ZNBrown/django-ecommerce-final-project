from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class Member(AbstractUser):
    username = None
    seller_nonce = models.TextField(default="Z40ehETBuVQ2BQGsiKqmsDmTHNTVI8r9H5Fh86doKwXkpvABUdcxH4pXYP")
    authcode = models.TextField(null=True, blank=True)
    sharedId = models.TextField(null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

#TODO: change user model to deal with emails for logging in primarily
#or at least return email right
    def __str__(self):
        return f'{self.email}'


class Basket(models.Model):
    user_id = models.OneToOneField(Member, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f'{self.user_id}'    
