# Generated by Django 4.0.4 on 2022-04-22 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itineraires', '0007_itineraire_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itineraire',
            name='altitudeDepart',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='itineraire',
            name='altitudeMax',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='itineraire',
            name='deniveleNegatif',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='itineraire',
            name='denivelePositif',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
