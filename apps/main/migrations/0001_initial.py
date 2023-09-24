# Generated by Django 4.2.5 on 2023-09-21 15:53

import apps.main.utility
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlackListProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=512, verbose_name='Модел')),
                ('imei1', models.CharField(max_length=100, verbose_name='IMEI 1')),
                ('sku', models.CharField(max_length=512, verbose_name='SKU')),
            ],
        ),
        migrations.CreateModel(
            name='Cashbek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('price', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('types', models.IntegerField(choices=[(1, 'Начисление Кэшбэка'), (2, 'Cписание Кэшбэка')])),
                ('user_phone', models.CharField(blank=True, max_length=1024, null=True)),
                ('description', models.CharField(blank=True, default='', max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_uz', models.CharField(max_length=256)),
                ('question_ru', models.CharField(max_length=256)),
                ('answer_uz', models.CharField(max_length=2400)),
                ('answer_ru', models.CharField(max_length=2400)),
            ],
        ),
        migrations.CreateModel(
            name='Fribase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fr_id', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title_uz', models.CharField(max_length=256)),
                ('title_ru', models.CharField(max_length=256)),
                ('body_uz', models.TextField(max_length=1000)),
                ('body_ru', models.TextField(max_length=1000)),
                ('image', models.ImageField(blank=True, null=True, upload_to='notifications/')),
            ],
        ),
        migrations.CreateModel(
            name='PriceProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_price', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата Добавлена')),
                ('model', models.CharField(max_length=512, verbose_name='Модел')),
                ('imei1', models.CharField(max_length=100, unique=True, verbose_name='IMEI 1')),
                ('sku', models.CharField(max_length=512, verbose_name='SKU')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=512)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('budget', models.IntegerField()),
                ('status', models.CharField(choices=[('wait', 'Ожидает одобрения модератором CashBek'), ('active', 'Активный'), ('refused', 'Отклоненный'), ('pause', 'Пауза'), ('finish', 'Завершенный')], default='wait', max_length=10)),
                ('description', models.CharField(default='', max_length=1024)),
                ('who', models.CharField(default='', max_length=1024)),
                ('price_procent', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QR_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_id', models.UUIDField(default=uuid.uuid4)),
                ('expiry_date', models.DateTimeField(null=True)),
                ('is_used', models.BooleanField(default=False)),
                ('types', models.IntegerField(choices=[(1, 'Начисление Кэшбэка'), (2, 'Cписание Кэшбэка')])),
                ('message_id', models.CharField(max_length=100, null=True)),
                ('chat_id', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReadNot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TempPriceProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TempPromo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('budget', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Token_confirm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=apps.main.utility.get_random_token, max_length=16)),
                ('expiry_date', models.DateTimeField(null=True)),
                ('is_used', models.BooleanField(default=False)),
                ('types', models.IntegerField(choices=[(1, 'Начисление Кэшбэка'), (2, 'Cписание Кэшбэка')])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.products')),
            ],
        ),
    ]
