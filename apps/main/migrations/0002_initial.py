# Generated by Django 4.2 on 2023-08-28 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='temppromo',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.vendor_account'),
        ),
        migrations.AddField(
            model_name='temppriceproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.products'),
        ),
        migrations.AddField(
            model_name='temppriceproduct',
            name='promo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.temppromo'),
        ),
        migrations.AddField(
            model_name='qr_code',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.products'),
        ),
        migrations.AddField(
            model_name='promo',
            name='products',
            field=models.ManyToManyField(related_name='promo', to='main.products'),
        ),
        migrations.AddField(
            model_name='promo',
            name='ven',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.vendor'),
        ),
        migrations.AddField(
            model_name='promo',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.vendor_account'),
        ),
        migrations.AddField(
            model_name='products',
            name='ven',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.vendor'),
        ),
        migrations.AddField(
            model_name='products',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.vendor_account'),
        ),
        migrations.AddField(
            model_name='priceproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.products'),
        ),
        migrations.AddField(
            model_name='priceproduct',
            name='promo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.promo'),
        ),
        migrations.AddField(
            model_name='cashbek',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.products'),
        ),
        migrations.AddField(
            model_name='cashbek',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.seller'),
        ),
        migrations.AddField(
            model_name='cashbek',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.simpleusers'),
        ),
        migrations.AddField(
            model_name='cashbek',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.vendor'),
        ),
        migrations.AddField(
            model_name='blacklistproducts',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.vendor_account'),
        ),
    ]