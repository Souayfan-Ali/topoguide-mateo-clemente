from django.urls import path

from . import views
"""
Urls pour l'application itinéraires
"""
app_name = 'itineraires'
urlpatterns = [
    path('', views.ItineraireListView.as_view(),name='liste_itineraires'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('sortie/<int:pk>/', views.SortieView.as_view(), name='sortie'),
    path('sortie/creation/', views.CreationSortie, name='creation_sortie'),
    path('sortie/modification/<int:sortie_id>', views.ModificationSortie, name='modification_sortie'),
    path('sortie/suppression/<int:sortie_id>', views.SuppressionSortie, name='suppression_sortie'),
    path('searchResults/', views.SearchResults, name='searchResults'),

]
