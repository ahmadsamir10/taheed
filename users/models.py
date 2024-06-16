from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from users.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name="اسم المستخدم")
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="الاسم الكامل")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الهاتف")

    is_active = models.BooleanField(default=True, verbose_name="نشط")
    is_staff = models.BooleanField(default=False, verbose_name="موظف")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    class Meta:
        verbose_name = "مستخدم لوحة التحكم"
        verbose_name_plural = "مستخدمين لوحة التحكم"

class Client(models.Model):
    STEPS_CHOICES = (
        ('first', 'الاولى'),
        ('second', 'الثانية'),
        ('completed', 'مكتمل ✅')
    )
    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="الاسم الكامل")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الهاتف")
    id_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الهوية")
    bike_count = models.IntegerField(default=0, verbose_name="عدد الدراجات")
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True, verbose_name="الإيصال")
    verification_code = models.CharField(max_length=6, blank=True, null=True, verbose_name="رمز التحقق")
    is_verified = models.BooleanField(default=False, verbose_name="تم التحقق")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    steps = models.CharField(max_length=20, choices=STEPS_CHOICES, verbose_name="الخطوات")
    
    class Meta:
        verbose_name = "العميل"
        verbose_name_plural = "العملاء"
        
        

class Motorcycle(models.Model):
    motorcycle_price = models.FloatField(verbose_name="سعر الدراجة النارية")
    available_motorcycles = models.PositiveIntegerField(default=0, verbose_name="الدراجات المتاحة")
    soldout_motorcycles = models.PositiveIntegerField(default=0, verbose_name="الدراجات المباعة")
    total_rental_amount = models.FloatField(default=0, verbose_name="إجمالي مبلغ الإيجار")
    
    def save(self, *args, **kwargs) -> None:
        self.total_rental_amount = self.soldout_motorcycles * self.motorcycle_price
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "معلومات الدراجات النارية"
        verbose_name_plural = "معلومات الدراجات النارية"
        

class Settings(models.Model):
    agreement_text = models.TextField(verbose_name="نص الاتفاق")
    bank_name = models.CharField(max_length=255, verbose_name="اسم البنك")
    bank_account_number = models.CharField(max_length=255, verbose_name="رقم الحساب البنكي")
        
    class Meta:
        verbose_name = "الاعدادات"
        verbose_name_plural = "الاعدادات"
        
