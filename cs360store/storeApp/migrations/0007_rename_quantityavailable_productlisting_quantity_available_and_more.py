# Generated by Django 4.0.3 on 2022-03-27 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0006_remove_producttag_product_remove_servicetag_service_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productlisting',
            old_name='quantityAvailable',
            new_name='quantity_available',
        ),
        migrations.RenameField(
            model_name='servicelisting',
            old_name='daysAvailable',
            new_name='days_available',
        ),
        migrations.RenameField(
            model_name='servicelisting',
            old_name='serviceArea',
            new_name='service_area',
        ),
    ]
