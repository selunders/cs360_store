# Generated by Django 4.0.3 on 2022-04-05 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0024_rename_user_cartproduct_cart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storeApp.cart'),
        ),
        migrations.AlterField(
            model_name='cartservice',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storeApp.cart'),
        ),
    ]
