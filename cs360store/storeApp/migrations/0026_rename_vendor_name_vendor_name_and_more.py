# Generated by Django 4.0.3 on 2022-04-12 20:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0025_alter_cartproduct_cart_alter_cartservice_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='vendor_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='quantity',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9999)]),
        ),
        migrations.AlterField(
            model_name='invoiceproduct',
            name='quantity_ordered',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(9999)]),
        ),
        migrations.AlterField(
            model_name='invoiceservice',
            name='status',
            field=models.CharField(blank=True, choices=[('sc', 'Scheduled'), ('cl', 'Canceled'), ('fl', 'Fulfilled')], default='sc', help_text='Order Status', max_length=2),
        ),
    ]