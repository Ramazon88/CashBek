# Generated by Django 4.2 on 2023-08-21 09:14

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='qr_code',
            name='chat_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='qr_code',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 21, 14, 16, 46, 170800)),
        ),
        migrations.AlterField(
            model_name='qr_code',
            name='qr_id',
            field=models.UUIDField(default=uuid.UUID('0f4c4ef9-2229-4b0b-90f8-e4a0a626de96')),
        ),
    ]