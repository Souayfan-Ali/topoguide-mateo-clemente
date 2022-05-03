from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views import generic
from itineraires.models import Itineraire, Sortie
from .forms import SortieForm

"""Toutes les vues affichent une barre de navigation à part le login"""


class ItineraireListView(generic.ListView):
    """ 
    Vue de la liste des itinéraires.
    """
    model = Itineraire


class DetailView(generic.DetailView):

    """
    Vue représentant : 
     - les détails de l'itinéraire choisi.
     - la liste des sorties sur cet itinéraire.

    """
    model = Itineraire


    #redéfinir get_context_data permet d'accéder aux sorties voulues
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liste_sorties"] = Sortie.objects.filter(
            itineraire__id=self.object.id)
        return context


class SortieView(generic.DetailView):
    """
    Vue représentant les sorties.
    Accessible par url direct mais inutile : on retrouve toutes les données nécéssaires dans DetailView.
    """
    model = Sortie
    template_name = 'itineraires/sorties.html'


@login_required
def CreationSortie(request):
    """
    Vue de création d'une sortie, en passant par les forms génériques de Django.

    """

    if request.method == 'GET':
        form = SortieForm()
    elif request.method == 'POST':
        form = SortieForm(request.POST)
        if form.is_valid():
            form.instance.randonneur = request.user
            form.save()
            #ce redirect renvoie vers l'itinéraire où l'on se trouvait avant la création de sortie
            return redirect('itineraires:detail', pk=form.cleaned_data['itineraire'].id) 
    return render(request, 'itineraires/creation_sortie.html', {'form': form})


@login_required
def ModificationSortie(request, sortie_id):
    """
    Vue de modification d'une sortie, relativement similaire a la création.

    """

    #ici on vérifie que l'utilisateur qui modifie est le bon
    #Pas forcément utile pour un utilisateur normal car inaccessible dans le cas posant probleme sans trifouiller les urls, on n'est jamais trop prudents
    sortie = Sortie.objects.get(pk=sortie_id)
    if request.user != sortie.randonneur:
        return redirect('itineraires:detail', pk=sortie.itineraire.id)
    if request.method == 'GET':
        form = SortieForm(instance=sortie)
    elif request.method == 'POST':
        form = SortieForm(request.POST, instance=sortie)
        if form.is_valid():
            form.save()
            #ce redirect renvoie vers l'itinéraire où l'on se trouvait avant la modification de sortie
            return redirect('itineraires:detail', pk=form.cleaned_data['itineraire'].id)
    return render(request, 'itineraires/modification_sortie.html', {'form': form})

@login_required
def SuppressionSortie(request,sortie_id):
    """
    Vue de suppression d'une sortie, relativement similaire a la création.

    """  
    #ici on vérifie que l'utilisateur qui modifie est le bon
    sortie = Sortie.objects.get(pk=sortie_id)
    if request.user != sortie.randonneur:
        return redirect('itineraires:detail', pk=sortie.itineraire.id)
    #on garde l'id avant de supprimer pour pouvoir rediriger vers une page cohérente
    s_id = sortie.itineraire.id
    sortie.delete()
    return redirect('itineraires:detail', pk=s_id)


def SearchResults(request):
    """
    Vue qui affiche les résultats de la recherche
    
    """
    #Initialisation de la variable de contexte
    context = {}

    #Si une recherche a été effectuée on renvoie les résulats sur la page searchResults.html
    if request.method == "POST":

        #On récupères les données du formulaire de recherche
        key_word = request.POST.get("search")
        filtre = request.POST.get("filtre")
        context["key_word"]=key_word
        context["filtre"]=filtre

        #Si l'utilisateur n'a pas entrée de mot (directement cliqué sur ok) on ne prend pas la peine de chercher
        #un résulat correspondant
        if key_word == "" or key_word == " ":
            render(request, "itineraires/searchResults.html", context)

        #Si le filtre est sur "aucun" on récupère les sorties les itinéraires et les commentaires où le mot clé apparaît
        if(filtre == "aucun"):
            liste_itinineraires = Itineraire.get_from_key_word(key_word)
            liste_sorties = Sortie.get_from_key_word(key_word)
            liste_commentaires = []

        #Si on filtre sur la date on récupère seulement les sorties ou le mot clé apparait et on trie par la date la liste des sorties
        if(filtre == "date-recente" or filtre == "date-ancienne"):
            liste_sorties = Sortie.get_from_key_word(key_word)
            liste_sorties = Sortie.filtrer(filtre, liste_sorties)
            liste_itinineraires = []
            liste_commentaires = []

        #Si on filtre sur la popularite/difficultée/durée/niveau d'expérience on récupère les itinéraires ou le mot clé apparait et on trie ces listes
        if(filtre == "popularite-decroissante"
         or filtre == "difficultee-croissante-moy"
         or filtre == "duree-croissante-moy"
         or filtre == "niveau-exp-decroissant-moy"):
            liste_itinineraires = Itineraire.get_from_key_word(key_word)
            liste_itinineraires = Itineraire.filtrer(filtre, liste_itinineraires)
            liste_sorties = []
            liste_commentaires = []

        
        #Mise à jour des context
        context["liste_itinineraires"]=liste_itinineraires
        context["liste_sorties"]=liste_sorties
        context["liste_commentaires"]=liste_commentaires

        
    return render(request, "itineraires/searchResults.html", context)
