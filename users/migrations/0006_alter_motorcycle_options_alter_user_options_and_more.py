# Generated by Django 5.0.6 on 2024-06-15 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_settings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='motorcycle',
            options={'verbose_name': 'معلومات الدراجات النارية', 'verbose_name_plural': 'معلومات الدراجات النارية'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'مستخدم لوحة التحكم', 'verbose_name_plural': 'مستخدمين لوحة التحكم'},
        ),
        migrations.AlterField(
            model_name='client',
            name='bike_count',
            field=models.IntegerField(default=0, verbose_name='عدد الدراجات'),
        ),
        migrations.AlterField(
            model_name='client',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء'),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='البريد الإلكتروني'),
        ),
        migrations.AlterField(
            model_name='client',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='الاسم الكامل'),
        ),
        migrations.AlterField(
            model_name='client',
            name='id_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='رقم الهوية'),
        ),
        migrations.AlterField(
            model_name='client',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='تم التحقق'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='رقم الهاتف'),
        ),
        migrations.AlterField(
            model_name='client',
            name='receipt',
            field=models.FileField(blank=True, null=True, upload_to='receipts/', verbose_name='الإيصال'),
        ),
        migrations.AlterField(
            model_name='client',
            name='steps',
            field=models.CharField(choices=[('first', 'الاولى'), ('second', 'الثانية'), ('completed', 'مكتمل ✅')], max_length=20, verbose_name='الخطوات'),
        ),
        migrations.AlterField(
            model_name='client',
            name='verification_code',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='رمز التحقق'),
        ),
        migrations.AlterField(
            model_name='motorcycle',
            name='available_motorcycles',
            field=models.PositiveIntegerField(default=0, verbose_name='الدراجات المتاحة'),
        ),
        migrations.AlterField(
            model_name='motorcycle',
            name='motorcycle_price',
            field=models.FloatField(verbose_name='سعر الدراجة النارية'),
        ),
        migrations.AlterField(
            model_name='motorcycle',
            name='soldout_motorcycles',
            field=models.PositiveIntegerField(default=0, verbose_name='الدراجات المباعة'),
        ),
        migrations.AlterField(
            model_name='motorcycle',
            name='total_rental_amount',
            field=models.FloatField(default=0, verbose_name='إجمالي مبلغ الإيجار'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='agreement_text',
            field=models.TextField(verbose_name='نص الاتفاق'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='bank_account_number',
            field=models.CharField(max_length=255, verbose_name='رقم الحساب البنكي'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='bank_name',
            field=models.CharField(max_length=255, verbose_name='اسم البنك'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='البريد الإلكتروني'),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='الاسم الكامل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='نشط'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='موظف'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='رقم الهاتف'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المستخدم'),
        ),
    ]