from django.contrib import admin
from .models import Itineraire, Sortie
# Register your models here.

# classe des itinéraires
class ItineraireAdmin(admin.ModelAdmin):
    #inutile d'afficher tous les champs
    list_display = ('id', 'nom', 'duree', 'difficulte')


admin.site.register(Itineraire, ItineraireAdmin)


# classe des sorties
class SortieAdmin(admin.ModelAdmin):
    #la plupart des champs pourraient être utilisés, on les met tous
    list_display = ('id', 'randonneur', 'itineraire', 'date_sortie', 'duree',
                    'difficulte', 'nbParticipants', 'experience', 'meteo')


admin.site.register(Sortie, SortieAdmin)
