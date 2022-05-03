
from dataclasses import fields
from django import forms
from .models import Commentaire, Image, Sortie


class SortieForm(forms.ModelForm):
    """
    Form générique de django utilisé pour création et modification
    """
    class Meta:
        # l'utilisateur a la main sur tout sauf le nom randonneur qui est lié à l'utilisateur connecté
        exclude = ('randonneur',)
        model = Sortie
        fields = '__all__'  # ['name']


class ImageForm(forms.ModelForm):
    """
    Form d'ajout de photo pour les sorties
    """

    # nécéssaire pour que l'on puisse modifier une sortie sans forcément ajouter de photo
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

    class Meta:
        # la sortie sera associée automatiquement
        model = Image
        fields = ['image', ]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True, 'name': 'images'})
        }


class CommentaireForm(forms.ModelForm):

    class Meta:
        model = Commentaire
        fields = ['texte']
