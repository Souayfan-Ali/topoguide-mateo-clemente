# Generated by Django 4.0.4 on 2022-05-03 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('itineraires', '0011_alter_image_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentaire', models.TextField()),
                ('date', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(1, 'Public'), (2, 'Cache'), (3, 'Prive')])),
                ('sortie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itineraires.sortie')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]