from django.contrib import admin
from .models import Itineraire
# Register your models here.



class ItineraireAdmin(admin.ModelAdmin):
    fields = ['name', 'duration','difficulty']
    list_display = ('name', 'duration','difficulty')

admin.site.register(Itineraire, ItineraireAdmin)

