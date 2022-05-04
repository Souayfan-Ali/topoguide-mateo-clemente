# Generated by Django 4.0.4 on 2022-05-02 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itineraires', '0009_alter_itineraire_coordonne_y_itineraire_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itineraire',
            name='Coordonne_Y_Itineraire',
            field=models.DecimalField(decimal_places=7, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='itineraire',
            name='Coordonne_Y_pointDeDepart',
            field=models.DecimalField(decimal_places=7, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='itineraire',
            name='Coordonne_x_Itineraire',
            field=models.DecimalField(decimal_places=7, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='itineraire',
            name='Coordonne_x_pointDeDepart',
            field=models.DecimalField(decimal_places=7, default=0, max_digits=10, null=True),
        ),
    ]
