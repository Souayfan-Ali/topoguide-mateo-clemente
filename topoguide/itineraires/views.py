import sys
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from datetime import datetime
from itineraires.models import Itineraire, Sortie, Image, Commentaire
from .forms import CommentaireForm, ImageForm, SortieForm, StatusForm
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
"""Toutes les vues affichent une barre de navigation à part le login"""


class ItineraireListView(generic.ListView):
    """
    Vue de la liste des itinéraires.
    """
    model = Itineraire


class DetailView(generic.UpdateView):

    """
    Vue représentant :
     - les détails de l'itinéraire choisi.
     - la liste des sorties sur cet itinéraire.

    """
    model = Itineraire
    template_name = 'itineraires/itineraire_detail.html'

    #nécéssaire pour pouvoir faire un formmixin dans une vue générique
    fileds = ['texte']
    form_class = CommentaireForm

    #on doit définir l'url de redirection en cas de form validé
    def get_success_url(self) -> str:
        #en cas de succes du form, on est redirigés vers l'itinéraire correspondant
        return '{}#itineraires'.format(reverse('itineraires:detail', kwargs={'pk': self.object.id}))

    # redéfinir get_context_data permet d'accéder aux sorties voulues
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #utilisateur
        context['user']=self.request.user

        #sorties associées à l'itinéraire
        context["liste_sorties"] = Sortie.objects.filter(
            itineraire__id=self.object.id
        )

        #commentaires associées à l'itinéraire
        context["commentaires"] = Commentaire.objects.filter(
            itineraire__id=self.object.id
        )

        #toutes les images des sorties sur cet itinéraire
        context['photos'] = Image.objects.filter(
            sortie__itineraire__id=self.object.id
        )

        #form de nouveau commentaire
        context['form'] = CommentaireForm(initial={
                                          'utilisateur': self.request.user, 'itineraire': self.object, 'date': datetime.now(), 'status': 1})
        #form de changement de status
        context['status_form'] = StatusForm()
        return context




    #seuls les utilisateurs connectés peuvent POSTer des données
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        #si le form POSTé est un changement de status
        if 'status' in request.POST:

            #recherche du commentaire sur lequel on veut effectuer le changement
            for com in Commentaire.objects.filter(itineraire__id=self.object.id):
                if "status-form-"+str(com.id) in request.POST:
                    com_id = com.id
                    break

            modified_com = Commentaire.objects.get(pk=com_id)

            form = StatusForm(request.POST,instance=modified_com)
 
            if request.user != modified_com.utilisateur:
                return self.form_invalid(form)
            #récupération de l'instance associée
            
            #validation
            if form.is_valid():
                com.status = request.POST['status']
                com.save()
                return HttpResponseRedirect(self.get_success_url())
        
        #si le form POSTé est un nouveau commentaire
        else:
            #récupération le form d commentaire avec la méthode django associée à form_class
            form = self.get_form()

            #validation
            if form.is_valid():
                Commentaire.objects.create(texte=form.cleaned_data['texte'],utilisateur=self.request.user, itineraire=self.object, date=datetime.now(), status=1)
                return self.form_valid(form)
        
        return self.form_invalid(form)
   

class SortieView(generic.DetailView):
    """
    Vue représentant les sorties.
    Accessible par url direct mais peu utile : on retrouve toutes les données nécéssaires dans DetailView.
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
            # ce redirect renvoie vers l'itinéraire où l'on se trouvait avant la création de sortie
            return redirect('itineraires:detail', pk=form.cleaned_data['itineraire'].id)
    return render(request, 'itineraires/creation_sortie.html', {'form': form})


@login_required
def ModificationSortie(request, sortie_id):
    """
    Vue de modification d'une sortie, relativement similaire a la création.

    """

    # ici on vérifie que l'utilisateur qui modifie est le bon
    # Pas forcément utile pour un utilisateur normal car inaccessible dans le cas posant probleme sans trifouiller les urls, on n'est jamais trop prudents
    sortie_instance = Sortie.objects.get(pk=sortie_id)
    if request.user != sortie_instance.randonneur:
        return redirect('itineraires:detail', pk=sortie_instance.itineraire.id)
    if request.method == 'GET':
        form = SortieForm(instance=sortie_instance)
        imgForm = ImageForm(request.POST, request.FILES)
    elif request.method == 'POST':
        form = SortieForm(request.POST, instance=sortie_instance)
        imgForm = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if imgForm.is_valid():
                # pour chaque image donnee on cree un objet
                images = request.FILES.getlist('images')
                for im in images:
                    Image.objects.create(
                        sortie=sortie_instance,
                        image=im
                    )
            # ce redirect renvoie vers l'itinéraire où l'on se trouvait avant la modification de sortie
            return redirect('itineraires:detail', pk=form.cleaned_data['itineraire'].id)
    return render(request, 'itineraires/modification_sortie.html', {'form': form, 'imgForm': imgForm})


@login_required
def SuppressionSortie(request, sortie_id):
    """
    Vue de suppression d'une sortie, relativement similaire a la création.

    """
    # ici on vérifie que l'utilisateur qui modifie est le bon
    sortie = Sortie.objects.get(pk=sortie_id)
    if request.user != sortie.randonneur:
        return redirect('itineraires:detail', pk=sortie.itineraire.id)
    # on garde l'id avant de supprimer pour pouvoir rediriger vers une page cohérente
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
            liste_itinineraires = Itineraire.organise_list(liste_itinineraires)

        #Si on filtre sur la date on récupère seulement les sorties ou le mot clé apparait et on trie par la date la liste des sorties
        if(filtre == "date-recente" or filtre == "date-ancienne"):
            liste_sorties = Sortie.get_from_key_word(key_word)
            liste_sorties = Sortie.filtrer(filtre, liste_sorties)
            liste_itinineraires = []
            liste_commentaires = []

        #Si on filtre sur la popularite/difficultée/durée/niveau d'expérience on récupère les itinéraires 
        #ou le mot clé apparait et on trie ces listes
        if(filtre == "popularite-decroissante"
         or filtre == "difficultee-croissante-moy"
         or filtre == "duree-croissante-moy"
         or filtre == "niveau-exp-croissant-moy"):
            liste_itinineraires = Itineraire.get_from_key_word(key_word)
            liste_itinineraires = Itineraire.filtrer(filtre, liste_itinineraires)
            liste_itinineraires = Itineraire.organise_list(liste_itinineraires)
            liste_sorties = []
            liste_commentaires = []

        
        #Mise à jour des context
        context["liste_itinineraires"]=liste_itinineraires
        context["liste_sorties"]=liste_sorties
        context["liste_commentaires"]=liste_commentaires

        
    return render(request, "itineraires/searchResults.html", context)
@login_required
def SuppressionImage(request, image_id):
    """
    Vue de suppression d'une sortie, relativement similaire a la création.

    """
    # ici on vérifie que l'utilisateur qui modifie est le bon
    image = Image.objects.get(pk=image_id)
    if request.user != image.sortie.randonneur:
        return redirect('itineraires:detail', pk=image.sortie.itineraire.id)
    image.delete()

    return redirect('itineraires:detail', pk=image.sortie.itineraire.id)
