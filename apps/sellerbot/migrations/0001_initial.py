# Generated by Django 4.2 on 2023-08-15 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SellerTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.CharField(max_length=100)),
                ('qr_type', models.IntegerField(null=True)),
                ('imei', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]