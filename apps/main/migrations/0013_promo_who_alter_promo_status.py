# Generated by Django 4.2 on 2023-07-20 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_promo_description_alter_promo_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='who',
            field=models.CharField(default='', max_length=1024),
        ),
        migrations.AlterField(
            model_name='promo',
            name='status',
            field=models.CharField(choices=[('wait', 'Ожидает одобрения модератором CashBek'), ('active', 'Активный'), ('refused', 'Отклоненный'), ('pause', 'Пауза'), ('finish', 'Завершенный')], default='wait', max_length=10),
        ),
    ]