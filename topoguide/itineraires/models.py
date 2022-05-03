from tkinter import CASCADE
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.views import generic
from django.contrib.auth.models import User

"""
Seulement deux modeles liés :
 - itinéraires
 - Sorties
"""


class Itineraire(models.Model):
    #certaines informations sont facultatives et seront affichées comme non connues dans le template associé
    nom = models.CharField(max_length=200)

    duree = models.DurationField()
    #les validators permettent de borner directement les valeurs
    difficulte = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    pointDeDepart = models.CharField(max_length=200,null=True)
    altitudeDepart = models.IntegerField(default=0,null=True)
    altitudeMax = models.IntegerField(default=0,null=True)
    denivelePositif = models.IntegerField(default=0,null=True)
    deniveleNegatif = models.IntegerField(default=0,null=True)
    description = models.TextField(null = True)
    def __str__(self):
        return self.nom


class Sortie(models.Model):
    #les validators permettent de borner directement les valeurs
    randonneur = models.ForeignKey(User, on_delete=models.CASCADE)
    itineraire = models.ForeignKey(Itineraire, on_delete=models.CASCADE)
    date_sortie = models.DateField(default=timezone.now)
    duree = models.DurationField()
    difficulte = models.IntegerField(default=0,
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    nbParticipants = models.IntegerField(validators=[MinValueValidator(1)])

    #format le plus répandu trouvé pour les choix django, pas seule possibilité
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

    def __str__(self):
        return self.itineraire.nom + " - " + self.randonneur.username
    

def itineraire_img_name(instance, filename):
    return ('/'.join([instance.sortie.itineraire.nom, filename])).replace(' ','_')


class Image(models.Model):
    sortie = models.ForeignKey(Sortie,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=itineraire_img_name,null=False)

class Commentaire(models.Model):
    utilisateur = models.ForeignKey(User,on_delete=models.CASCADE)
    texte = models.TextField()
    date = models.DateTimeField()
    itineraire = models.ForeignKey(Itineraire,on_delete=models.CASCADE)

    PB = 1
    HID = 2
    PV = 3
    typeStatus = [
      (PB,'Public'),
      (HID,'Cache'),
      (PV,'Prive')
    ]

    status = models.IntegerField(choices=typeStatus)
    


