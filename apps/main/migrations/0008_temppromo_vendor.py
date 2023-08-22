# Generated by Django 4.2 on 2023-07-05 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_vendor_price'),
        ('main', '0007_promo_create_at_promo_price_procent'),
    ]

    operations = [
        migrations.AddField(
            model_name='temppromo',
            name='vendor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.vendor_account'),
            preserve_default=False,
        ),
    ]