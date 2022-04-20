from django.urls import path

from . import views




app_name = 'itineraires'
urlpatterns = [
    path('', views.ItineraireListView.as_view(),name='liste_itineraires'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('sortie/<int:pk>/', views.SortieView.as_view(), name='sortie'),
    path('sortie/creation/', views.CreationSortie, name='creation_sortie'),
    path('sortie/modification/<int:sortie_id>', views.ModificationSortie, name='modification_sortie'),

]
