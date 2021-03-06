# Generated by Django 4.0.3 on 2022-03-30 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0011_alter_productlisting_imageurl_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicelisting',
            name='imageURL',
            field=models.URLField(blank='True', default='https://picsum.photos/400/300', help_text='Enter image URL', null=True),
        ),
        migrations.AlterField(
            model_name='servicelisting',
            name='name',
            field=models.CharField(help_text='Enter a name for your service.', max_length=200),
        ),
    ]
