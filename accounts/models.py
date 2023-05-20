from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from rest_framework.authtoken.models import Token

# Create your models here.
class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, phone_no, password, **extra_fields):
        """
        Create and save a User with the given email and password instead of username.
        """
        if not phone_no:
            raise ValueError('The Phone number must be set')
        user = self.model(phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_no, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone_no, password, **extra_fields)

class User(AbstractUser):
    username=None

    # extra fields
    email = models.EmailField(unique=True)
    name = models.CharField(max_length = 50)
    phone_no = models.CharField(unique=True, max_length = 10)
    company = models.CharField(max_length = 50, blank=True)
    isemployee = models.BooleanField(blank=True, default=False)

    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS=[]

    objects = UserManager()

    def __str__(self):
        return self.name

    @property
    def token(self):
        token = Token.objects.get(user=User.objects.get(self.id))
        return token
