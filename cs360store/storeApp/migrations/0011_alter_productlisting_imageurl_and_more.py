# Generated by Django 4.0.3 on 2022-03-30 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0010_alter_productlisting_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlisting',
            name='imageURL',
            field=models.URLField(default='https://picsum.photos/400/300', help_text='Enter image URL'),
        ),
        migrations.AlterField(
            model_name='servicelisting',
            name='name',
            field=models.CharField(default='https://picsum.photos/400/300', help_text='Enter a name for your service.', max_length=200),
        ),
    ]
