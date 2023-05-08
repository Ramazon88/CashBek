# Generated by Django 4.2 on 2023-05-08 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userconfirmation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='auth_status',
            field=models.CharField(choices=[('new', 'NEW'), ('code_verified', 'Code verified'), ('half_done', 'Done without MyID'), ('done', 'Done')], default='new', max_length=60),
        ),
        migrations.AlterField(
            model_name='historicaluser',
            name='user_type',
            field=models.CharField(choices=[('user', 'User'), ('vendor', 'Vendor'), ('manager', 'Manager'), ('seller', 'Seller')], default='user', max_length=60),
        ),
        migrations.AlterField(
            model_name='user',
            name='auth_status',
            field=models.CharField(choices=[('new', 'NEW'), ('code_verified', 'Code verified'), ('half_done', 'Done without MyID'), ('done', 'Done')], default='new', max_length=60),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('user', 'User'), ('vendor', 'Vendor'), ('manager', 'Manager'), ('seller', 'Seller')], default='user', max_length=60),
        ),
    ]
