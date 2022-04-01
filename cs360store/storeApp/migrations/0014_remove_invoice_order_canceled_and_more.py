# Generated by Django 4.0.3 on 2022-03-31 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0013_remove_invoice_vendor_invoice_order_canceled_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='order_canceled',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='order_fulfilled',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='order_shipped',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='payment_amount',
        ),
        migrations.AddField(
            model_name='invoiceproduct',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invoiceproduct',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invoiceservice',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invoiceservice',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
