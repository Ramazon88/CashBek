# Generated by Django 4.2 on 2023-06-06 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_alter_vendor_account_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='GSM', max_length=512, verbose_name='Категория')),
                ('model', models.CharField(max_length=512, verbose_name='Модел')),
                ('sku', models.CharField(max_length=512, verbose_name='SKU')),
                ('imei1', models.CharField(max_length=100, unique=True, verbose_name='IMEI 1')),
                ('imei2', models.CharField(default='', max_length=100, verbose_name='IMEI 2')),
                ('status', models.CharField(default='', max_length=100, verbose_name='Статус')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.vendor')),
            ],
        ),
    ]