# Generated by Django 4.2 on 2023-06-06 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_manager_seller_simpleusers_vendor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_account',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to='users.vendor', verbose_name='Vendor'),
        ),
    ]
