from django.urls import include, path

from . import views




app_name = 'itineraires'
urlpatterns = [
    path('', views.ItineraireListView.as_view(),name='itinerairesList'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('sortie/<int:pk>/', views.SortieView.as_view(), name='sortie'),

]
