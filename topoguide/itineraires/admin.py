from django.contrib import admin
from .models import Itineraire,Sortie
# Register your models here.


class ItineraireAdmin(admin.ModelAdmin):
    list_display = ('id','nom', 'duree', 'difficulte')


admin.site.register(Itineraire, ItineraireAdmin)


class SortieAdmin(admin.ModelAdmin):

    list_display = ('id','randonneur', 'itineraire', 'date_sortie', 'duree',
                 'difficulte', 'nbParticipants', 'experience', 'meteo')

admin.site.register(Sortie,SortieAdmin)