from django import forms
from .models import Sortie

class SortieForm(forms.ModelForm):
    """
    Form générique de django utilisé pour création et modification
    """
    class Meta:
        #l'utilisateur a la main sur tout sauf le nom randonneur qui est lié à l'utilisateur connecté
        exclude = ('randonneur',)
        model = Sortie
        fields = '__all__' # ['name']
        