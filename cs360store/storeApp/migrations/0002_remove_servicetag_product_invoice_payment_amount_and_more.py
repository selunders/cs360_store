# Generated by Django 4.0.3 on 2022-03-27 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicetag',
            name='product',
        ),
        migrations.AddField(
            model_name='invoice',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='servicetag',
            name='service',
            field=models.ManyToManyField(blank=True, to='storeApp.servicelisting'),
        ),
        migrations.AlterField(
            model_name='productlisting',
            name='name',
            field=models.CharField(help_text='Enter a name for your product.', max_length=200),
        ),
        migrations.AlterField(
            model_name='producttag',
            name='product',
            field=models.ManyToManyField(blank=True, to='storeApp.productlisting'),
        ),
        migrations.AlterField(
            model_name='servicelisting',
            name='name',
            field=models.CharField(help_text='Enter a name for your service.', max_length=200),
        ),
    ]
