from django.urls import include, path

from . import views




app_name = 'itineraires'
urlpatterns = [
    path('', views.ItineraireListView.as_view(),name='itinerairesList'),
    path('', views.DetailView.as_view(),name='Detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

]
