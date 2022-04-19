from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.views import generic

# Create your models here.


class Itineraire(models.Model):

  name = models.CharField(max_length=200)
  duration = models.DurationField()
  difficulty = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])

  def __str__(self):
      return self.name

class DetailsView(generic.DetailView):
    model = Itineraire
    template_name = 'itineraires/details.html'
