from typing import Iterable
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from users.managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "المستخدم"
        verbose_name_plural = "المستخدمين"



class Client(models.Model):
    STEPS_CHOICES = (
        ('first', 'الاولى'),
        ('second', 'الثانية'),
        ('completed', 'مكتمل ✅')
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    id_number = models.CharField(max_length=20, blank=True, null=True)
    bike_count = models.IntegerField(default=0)
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    steps = models.CharField(max_length=20, choices=STEPS_CHOICES)
    
    class Meta:
        verbose_name = "العميل"
        verbose_name_plural = "العملاء"



class Motorcycle(models.Model):
    motorcycle_price = models.FloatField()
    available_motorcycles = models.PositiveIntegerField(default=0)
    soldout_motorcycles = models.PositiveIntegerField(default=0)
    total_rental_amount = models.PositiveIntegerField(default=0)
    
    
    def save(self, *args, **kwargs) -> None:
        self.total_rental_amount = self.soldout_motorcycles * self.motorcycle_price
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "الدراجة النارية"
        verbose_name_plural = "الدراجات النارية"