from ast import keyword
import datetime
from re import I
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
            -itineraires_key_word_all_list : une liste de double contenant 
            (0:tinéraire, 1:endroit ou le mot clé a été trouvé, 2:difficultee moyenne
            3:nombre de sorties associées, 4:durée moyenne sur les sorties, 5:experience moyenne, 6:afficher le titre(True) ou non(False))
        """

        #Recherche du mot clé dans les titres des itinéraires
        itineraires_key_word_in_title = Itineraire.objects.filter(nom__icontains=key_word)
        itineraires_key_word_in_title_list = [[itineraire, "title", itineraire.get_difficultee_moyenne(), itineraire.get_nb_sortie(), 
        itineraire.get_duree_moyenne(), itineraire.get_experience_moyenne(), True]
        for itineraire in itineraires_key_word_in_title]

        #Recherche du mot clé dans la description des itinéraires
        itineraires_key_word_in_description = Itineraire.objects.filter(description__icontains=key_word)
        itineraires_key_word_in_description_list = [[itineraire, "description", itineraire.get_difficultee_moyenne(), itineraire.get_nb_sortie(), 
        itineraire.get_duree_moyenne(), itineraire.get_experience_moyenne(), True ] 
        for itineraire in itineraires_key_word_in_description]        

        #recherche du mot clé dans le point de départ des itinéraires
        itineraires_key_word_in_pointDeDepart = Itineraire.objects.filter(pointDeDepart__icontains=key_word)
        itineraires_key_word_in_pointDeDepart_list = [[itineraire, "pointDeDepart",itineraire.get_difficultee_moyenne(), itineraire.get_nb_sortie(),
        itineraire.get_duree_moyenne(), itineraire.get_experience_moyenne(), True] 
        for itineraire in itineraires_key_word_in_pointDeDepart]        

        #Assemblage des itinéraires avec le mot clé dans une seule liste
        itineraires_key_word_all_list = itineraires_key_word_in_title_list + itineraires_key_word_in_description_list + itineraires_key_word_in_pointDeDepart_list

        return itineraires_key_word_all_list



    def get_nb_sortie(self):
        """
        Donne le nombre de sorties associé à un itinéraire
        """
        liste_sorties = Sortie.objects.filter(itineraire__nom=self.nom)
        return len(liste_sorties)


    def get_difficultee_moyenne(self):
        """
        Renvoie la difficultée moyenne de l'itinéraire (moyenne sur la difficultée des sorties)
        """
        liste_sorties = Sortie.objects.filter(itineraire__nom=self.nom)
        nb_sorties = len(liste_sorties)
        somme_difficultee = 0
        for sortie in liste_sorties:
            somme_difficultee += sortie.difficulte
        moyenne_difficultee = somme_difficultee/nb_sorties
        return moyenne_difficultee


    def get_duree_moyenne(self):
        """
        Renvoie la moyenne de la durée sur les sorties
        """
        liste_sorties = Sortie.objects.filter(itineraire__nom=self.nom)
        nb_sorties = len(liste_sorties)
        somme_duree_heure = 0
        for sortie in liste_sorties:
            somme_duree_heure += sortie.duree.seconds/3600
        moyenne_duree_min = int(somme_duree_heure%nb_sorties)
        moyenne_duree_heure = int(somme_duree_heure//nb_sorties)
        return datetime.time(hour=moyenne_duree_heure, minute=moyenne_duree_min)

    def get_experience_moyenne(self):
        """
        Retourne l'expérience moyenne des randonneurs qui ont fait la sortie
        """
        liste_sorties = Sortie.objects.filter(itineraire__nom=self.nom)
        somme_experience = 0
        nb_randonneurs = 0
        for sortie in liste_sorties:
            nb_randonneurs += sortie.nbParticipants
            somme_experience += sortie.experience*sortie.nbParticipants
        moyenne_experience = somme_experience/nb_randonneurs
        return moyenne_experience

    def organise_list(liste_itineraires):
        """
        Réorganise la liste des itinénaires pour éviter les doublons
        """
        liste_itineraires_new = []

        if not liste_itineraires:
            return liste_itineraires_new

       
        while liste_itineraires:
            
            itineraire_double = liste_itineraires.pop(0)
            liste_itineraires_new.append(itineraire_double)
            taille = len(liste_itineraires)

            i=0
            while i<taille:
                itineraire_double_actuel = liste_itineraires[i]
                if(itineraire_double_actuel[0].nom == itineraire_double[0].nom):
                    liste_itineraires.pop(i)
                    taille -=1
                    itineraire_double_actuel[6] = False
                    liste_itineraires_new.append(itineraire_double_actuel)
                else:
                    i+=1
        
        return liste_itineraires_new





    def filtrer(filtre, liste_itineraires):

        if not liste_itineraires:
            return liste_itineraires

        max_init = len(liste_itineraires)

        if (filtre == "popularite-decroissante"):

            liste_itineraire_triee_popularite_decroissante = []

            #On parcours tous les éléments de la liste des itineraires
            #Au rang k on a k éléments dans la liste triée et k-taille initiale dans la liste initiale
            for k in range(0,max_init):

                itineraire_max = liste_itineraires[0][0]
                value_max = itineraire_max.get_nb_sortie()
                indice_itineraire_max = 0
                

                #On trouve le plus petit élément de la liste non triée
                for i in range(1, len(liste_itineraires)):
                    itineraire_a_comparer = liste_itineraires[i][0]
                    valeur_a_comparer = itineraire_a_comparer.get_nb_sortie()

                    if(value_max < valeur_a_comparer):
                        itineraire_max = itineraire_a_comparer
                        value_max = valeur_a_comparer
                        indice_itineraire_max = i

                liste_itineraire_triee_popularite_decroissante.append(liste_itineraires.pop(indice_itineraire_max))
            
            return liste_itineraire_triee_popularite_decroissante

        if (filtre == "difficultee-croissante-moy"):

            liste_itineraire_triee_difficultee_croissante = []

            #On parcours tous les éléments de la liste des itineraires
            #Au rang k on a k éléments dans la liste triée et k-taille initiale dans la liste initiale
            for k in range(0,max_init):

                itineraire_min = liste_itineraires[0][0]
                value_min = itineraire_min.get_difficultee_moyenne()
                indice_itineraire_min = 0
                

                #On trouve le plus petit élément de la liste non triée
                for i in range(1, len(liste_itineraires)):
                    itineraire_a_comparer = liste_itineraires[i][0]
                    valeur_a_comparer = itineraire_a_comparer.get_difficultee_moyenne()


                    if(value_min > valeur_a_comparer):
                        itineraire_min = itineraire_a_comparer
                        value_min = valeur_a_comparer
                        indice_itineraire_min = i

                liste_itineraire_triee_difficultee_croissante.append(liste_itineraires.pop(indice_itineraire_min))
            
            return liste_itineraire_triee_difficultee_croissante

        if (filtre == "duree-croissante-moy"):

            liste_itineraire_triee_duree_croissante = []

            #On parcours tous les éléments de la liste des itineraires
            #Au rang k on a k éléments dans la liste triée et k-taille initiale dans la liste initiale
            for k in range(0,max_init):

                itineraire_min = liste_itineraires[0][0]
                value_min = itineraire_min.get_duree_moyenne()
                indice_itineraire_min = 0
                

                #On trouve le plus petit élément de la liste non triée
                for i in range(1, len(liste_itineraires)):
                    itineraire_a_comparer = liste_itineraires[i][0]
                    valeur_a_comparer = itineraire_a_comparer.get_duree_moyenne()

                    if(value_min > valeur_a_comparer):
                        itineraire_min = itineraire_a_comparer
                        value_min = valeur_a_comparer
                        indice_itineraire_min = i

                liste_itineraire_triee_duree_croissante.append(liste_itineraires.pop(indice_itineraire_min))
            
            return liste_itineraire_triee_duree_croissante

        if (filtre == "niveau-exp-decroissant-moy"):

            liste_itineraire_triee_experience_croissante = []

            #On parcours tous les éléments de la liste des itineraires
            #Au rang k on a k éléments dans la liste triée et k-taille initiale dans la liste initiale
            for k in range(0,max_init):

                itineraire_min = liste_itineraires[0][0]
                value_min = itineraire_min.get_experience_moyenne()
                indice_itineraire_min = 0
                

                #On trouve le plus petit élément de la liste non triée
                for i in range(1, len(liste_itineraires)):
                    itineraire_a_comparer = liste_itineraires[i][0]
                    valeur_a_comparer = itineraire_a_comparer.get_experience_moyenne()

                    if(value_min > valeur_a_comparer):
                        itineraire_min = itineraire_a_comparer
                        value_min = valeur_a_comparer
                        indice_itineraire_min = i

                liste_itineraire_triee_experience_croissante.append(liste_itineraires.pop(indice_itineraire_min))
            
            return liste_itineraire_triee_experience_croissante           




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

