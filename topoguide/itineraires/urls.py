from django.urls import include, path

from . import views
from django.views.generic import TemplateView




app_name = 'polls'
urlpatterns = [
    path('', TemplateView.as_view(template_name="itineraires/auth.html")),
]
