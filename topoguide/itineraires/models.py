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

        ARGUMENT :
            -key_word : str contenant le mot clé saisi dans la barre de recherche

        RETURN:
            -itineraires_key_word_all_list : une liste de double contenant (itinéraire, endroit ou le mot clé a été trouvé)
        """

        #Recherche du mot clé dans les titres des itinéraires
        itineraires_key_word_in_title = Itineraire.objects.filter(nom__icontains=key_word)
        itineraires_key_word_in_title_list = [(itineraire, "title") for itineraire in itineraires_key_word_in_title]

        #Recherche du mot clé dans la description des itinéraires
        itineraires_key_word_in_description = Itineraire.objects.filter(description__icontains=key_word)
        itineraires_key_word_in_description_list = [(itineraire, "description") for itineraire in itineraires_key_word_in_description]        

        #recherche du mot clé dans le point de départ des itinéraires
        itineraires_key_word_in_pointDeDepart = Itineraire.objects.filter(pointDeDepart__icontains=key_word)
        itineraires_key_word_in_pointDeDepart_list = [(itineraire, "pointDeDepart") for itineraire in itineraires_key_word_in_pointDeDepart]        

        #Assemblage des itinéraires avec le mot clé dans une seule liste
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



    def get_from_key_word(key_word):
        """
        Création d'une liste de double contenant la sortie avec le mot clé correspondant
        et l'endroit ou le mot clé a été trouvé
        
        ARGUMENT :
            -key_word : str contenant le mot clé saisi dans la barre de recherche

        RETURN:
            -sorties_key_word_all_list : une liste de double contenant (sortie, endroit ou le mot clé a été trouvé)
        """
        #Recherche du mot clé dans le nom des randonneur dans les sorties
        sorties_key_word_in_randonneur = Sortie.objects.filter(randonneur__username__icontains=key_word)
        sorties_key_word_in_randonneur_list = [(itineraire, "randonneur") for itineraire in sorties_key_word_in_randonneur]

        #Assemblage des sorties avec le mot clé dans une seule liste
        sortie_key_word_all_list = sorties_key_word_in_randonneur_list
      
        return sortie_key_word_all_list
    
    def filtrer(filtre, liste_sorties):
        """
        Trie la liste des sorties en fonction du filtre:
        -date-recente : les sorties de la plus récente à la plus ancienne
        -date-ancienne : les sorties de la plus ancienne à la plus récente

        ARGUMENTS:
            -filtre : le filtre choisit
            -liste_sorties : la liste des sorties à trier -> rappel [...(sortie_i, endroit où le mot clé à été trouvé)...]

        RETURN:
            -liste_sorties_triee = la liste (toujours la liste de double) triée en fonction du mot clé
        """

        #Si la liste des sortie est vide on ne l'a trie pas
        if not liste_sorties:
            return liste_sorties

        
        #Déclaration de la nouvelle liste triée
        liste_sorties_triee_dates_croissantes = []
        max_init = len(liste_sorties)


        #On parcours tous les éléments de la liste des sorties
        #Au rang k on a k éléments dans la liste triée et k-taille initiale dans la liste initiale
        for k in range(0,max_init):

            sortie_date_min = liste_sorties[0][0]
            date_min = sortie_date_min.date_sortie
            indice_sortie_min = 0

            #On trouve le plus petit élément de la liste non triée
            for i in range(1, len(liste_sorties)):
                sortie_a_comparer = liste_sorties[i][0]
                date_a_comparer = sortie_a_comparer.date_sortie

                if(date_min.year > date_a_comparer.year):
                    sortie_date_min = liste_sorties[i][0]
                    date_min = sortie_date_min.date_sortie
                    indice_sortie_min = i

                if (date_min.year == date_a_comparer.year and date_min > date_a_comparer):
                    sortie_date_min = liste_sorties[i][0]
                    date_min = sortie_date_min.date_sortie
                    indice_sortie_min = i

            liste_sorties_triee_dates_croissantes.append(liste_sorties.pop(indice_sortie_min))
            
        
        #Si le filtre est de la date la plus ancienne à la plus récente
        if filtre == "date-ancienne":
            return liste_sorties_triee_dates_croissantes

        #Si le filtre est de la date la plus récente à la plus ancienne
        liste_sorties_triee_dates_croissantes.reverse()
        return liste_sorties_triee_dates_croissantes

