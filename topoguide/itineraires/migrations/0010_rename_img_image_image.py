# Generated by Django 4.0.4 on 2022-04-25 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itineraires', '0009_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='img',
            new_name='image',
        ),
    ]
