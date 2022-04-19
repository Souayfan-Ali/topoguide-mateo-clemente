from django.views.generic import ListView
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views import generic
from itineraires.models import Itineraire

# Create your views here.


def auth(request):
  render(request,'itineraires/itineraires.html')

class ItineraireListView(ListView):
  model = Itineraire

class DetailView(generic.DetailView):
  model = Itineraire
