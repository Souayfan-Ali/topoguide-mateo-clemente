from email.mime import image
from sys import stderr
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views import generic
from itineraires.models import Itineraire, Sortie, Image
from .forms import ImageForm, SortieForm

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
            itineraire__id=self.object.id
        )
        context['photos'] = Image.objects.filter(
            sortie__itineraire__id = self.object.id
        )
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
    sortie_instance = Sortie.objects.get(pk=sortie_id)
    if request.user != sortie_instance.randonneur:
        return redirect('itineraires:detail', pk=sortie_instance.itineraire.id)
    if request.method == 'GET':
        form = SortieForm(instance=sortie_instance)
        imgForm = ImageForm(request.POST,request.FILES)
    elif request.method == 'POST':
        form = SortieForm(request.POST, instance=sortie_instance)
        imgForm = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            if imgForm.is_valid():
                #pour chaque image donnee on cree un objet
                images = request.FILES.getlist('images')
                for im in images:   
                    Image.objects.create(
                        sortie = sortie_instance,
                        image = im
                    )
            #ce redirect renvoie vers l'itinéraire où l'on se trouvait avant la modification de sortie
            return redirect('itineraires:detail', pk=form.cleaned_data['itineraire'].id)
    return render(request, 'itineraires/modification_sortie.html', {'form': form,'imgForm':imgForm})

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

@login_required
def SuppressionImage(request,image_id):
    """
    Vue de suppression d'une sortie, relativement similaire a la création.

    """  
    #ici on vérifie que l'utilisateur qui modifie est le bon
    image = Image.objects.get(pk=image_id)
    if request.user != image.sortie.randonneur:
        return redirect('itineraires:detail', pk=image.sortie.itineraire.id)
    #on garde l'id avant de supprimer pour pouvoir rediriger vers une page cohérente
    i_id = image.id
    image.delete()

    return redirect('itineraires:detail', pk=image.sortie.itineraire.id)





