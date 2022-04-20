from decimal import getcontext
from django.shortcuts import redirect,render
from django.views import generic
from itineraires.models import Itineraire, Sortie
from .forms import SortieForm

# Create your views here.


class ItineraireListView(generic.ListView):
    model = Itineraire


class DetailView(generic.DetailView):
  model = Itineraire

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["liste_sorties"] = Sortie.objects.filter(itineraire__id = self.object.id)
    return context


class SortieView(generic.DetailView):
    model = Sortie
    template_name = 'itineraires/sorties.html'


def CreationSortie(request):

    if request.method == 'GET':
        form = SortieForm()
    elif request.method == 'POST':
        form = SortieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('itineraires:liste_itineraires',args=1)
    return render(request, 'itineraires/creation_sortie.html', {'form': form})


def ModificationSortie(request, sortie_id):

    sortie = Sortie.objects.get(pk=sortie_id)
    if request.method == 'GET':
        form = SortieForm(instance=sortie)
    elif request.method == 'POST':
        form = SortieForm(request.POST, instance=sortie)
        if form.is_valid():
            form.save()
            return redirect('itineraires:detail',pk= form.cleaned_data['itineraire'].id)
    return render(request, 'itineraires/modification_sortie.html', {'form': form})
