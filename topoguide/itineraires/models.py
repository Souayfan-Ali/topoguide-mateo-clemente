from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.views import generic
from django.contrib.auth.models import User

# Create your models here.


class Itineraire(models.Model):

    name = models.CharField(max_length=200)
    duration = models.DurationField()
    difficulty = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return self.name


class DetailsView(generic.DetailView):
    model = Itineraire
    template_name = 'itineraires/details.html'


class Sortie(models.Model):
    randonneur = models.ForeignKey(User, on_delete=models.CASCADE)
    itineraire = models.ForeignKey(Itineraire, on_delete=models.CASCADE)
    date_sortie = models.DateField(default=datetime.now())
    duree = models.DurationField()
    difficulte = models.IntegerField(default=0,
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    nbParticipants = models.IntegerField(validators=[MinValueValidator(1)])

    DEB = 1
    MIXTE = 2
    EXP = 3
    niveaux = [
        (DEB, 'Débutants'),
        (MIXTE, 'Mixte'),
        (EXP, 'Expérimentés'),

    ]
    experience = models.IntegerField(choices=niveaux,)

    MV = 1
    MOY = 2
    BON = 3

    typeMeteo = [
      (MV,'Mauvaise'),
      (MOY,'Moyenne'),
      (BON,'Bonne')
    ]

    meteo = models.IntegerField(choices=typeMeteo)
