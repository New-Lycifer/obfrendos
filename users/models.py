from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password
from django.utils import timezone


"""
class User(AbstractUser):
    # Поле email, обязательное для заполнения и уникальное
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
"""

class LocalUser(AbstractUser, models.Model):
    groups = models.ManyToManyField(
        Group,
        verbose_name='Groups',
        blank=True,
        related_name="localuser_groups"  # Измененное имя обратного доступа для groups
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='User permissions',
        blank=True,
        related_name="localuser_user_permissions"  # Измененное имя обратного доступа для user_permissions
    )

    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bdate = models.DateField(null=True)
    email = models.CharField()
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    registerdate = models.DateTimeField(default=timezone.now)


    """
    def save(self, *args, **kwargs):
        # Перед сохранением хешируем пароль
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        # Проверяем соответствие пароля
        return make_password(raw_password) == self.password
    """