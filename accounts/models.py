from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, username=None, first_name=None, last_name=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")

        # For normal users: enforce required fields
        if not extra_fields.get('is_superuser', False):
            if not email:
                raise ValueError("The Email field must be set")

        # Default fallbacks for superusers
        email = email or f"{username}@admin.local"

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,


            
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username=username, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    )

    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=50 , default='')
    rank = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    
    


class Device(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='device')
    fcmToken = models.CharField(max_length=255, blank=True, null=True , unique=True)
    platformType = models.TextField(default="android" , blank=True, null=True)


