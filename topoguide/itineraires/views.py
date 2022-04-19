from decimal import getcontext
from django.shortcuts import get_object_or_404
from django.views import generic
from itineraires.models import Itineraire, Sortie

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
