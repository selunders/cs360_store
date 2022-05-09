# Generated by Django 4.0.3 on 2022-05-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeApp', '0029_alter_producttag_options_alter_servicetag_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='producttag',
            options={'ordering': ['-viewcount']},
        ),
        migrations.AlterModelOptions(
            name='servicetag',
            options={'ordering': ['-viewcount']},
        ),
        migrations.AlterField(
            model_name='productlisting',
            name='imageURL',
            field=models.URLField(default='https://picsum.photos/400/300?random=69936', help_text='Enter image URL'),
        ),
        migrations.AlterField(
            model_name='servicelisting',
            name='imageURL',
            field=models.URLField(blank='True', default='https://picsum.photos/400/300?random=89033', help_text='Enter image URL', null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='logoURL',
            field=models.URLField(default='https://picsum.photos/400/300?random=85409', help_text='Enter image URL'),
        ),
    ]
