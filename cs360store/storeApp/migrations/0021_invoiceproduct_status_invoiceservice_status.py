# Generated by Django 4.0.3 on 2022-04-01 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0020_alter_invoiceproduct_id_alter_invoiceservice_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceproduct',
            name='status',
            field=models.CharField(blank=True, choices=[('or', 'Order Received'), ('sh', 'Shipped')], default='or', help_text='Order Status', max_length=2),
        ),
        migrations.AddField(
            model_name='invoiceservice',
            name='status',
            field=models.CharField(blank=True, choices=[('sc', 'Scheduled'), ('cm', 'Completed')], default='sc', help_text='Order Status', max_length=2),
        ),
    ]