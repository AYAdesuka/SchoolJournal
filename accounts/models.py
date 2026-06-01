from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    PERSON_STATUS = [
        ('учитель', 'Учитель'),
        ('студент', 'Студент'),
        ('админ', 'Админ'),
    ]

    role = models.CharField(max_length=20, choices=PERSON_STATUS, default="student")
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
