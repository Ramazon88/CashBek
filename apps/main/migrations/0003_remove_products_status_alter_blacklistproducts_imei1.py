# Generated by Django 4.2 on 2023-06-13 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_blacklistproducts_remove_products_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='status',
        ),
        migrations.AlterField(
            model_name='blacklistproducts',
            name='imei1',
            field=models.CharField(max_length=100, verbose_name='IMEI 1'),
        ),
    ]
