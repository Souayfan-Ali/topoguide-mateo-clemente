from ast import keyword
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

    def get_from_key_word(key_word):
        """
        Création d'une liste de double contenant l'itinéraire avec le mot clé correspondant
        et l'endroit ou le mot clé a été trouvé
        """
        itineraires_key_word_in_title = Itineraire.objects.filter(nom__icontains=key_word)
        itineraires_key_word_in_title_list = [(itineraire, "title") for itineraire in itineraires_key_word_in_title]

        itineraires_key_word_in_description = Itineraire.objects.filter(description__icontains=key_word)
        itineraires_key_word_in_description_list = [(itineraire, "description") for itineraire in itineraires_key_word_in_description]        

        itineraires_key_word_in_pointDeDepart = Itineraire.objects.filter(pointDeDepart__icontains=key_word)
        itineraires_key_word_in_pointDeDepart_list = [(itineraire, "pointDeDepart") for itineraire in itineraires_key_word_in_pointDeDepart]        

        itineraires_key_word_all_list = itineraires_key_word_in_title_list + itineraires_key_word_in_description_list + itineraires_key_word_in_pointDeDepart_list

        return itineraires_key_word_all_list



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
