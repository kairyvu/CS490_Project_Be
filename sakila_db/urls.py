from django.urls import path
from . import views

urlpatterns = [
    path('api/films/top/', views.getTopFilms, name='getTopFilms'),
]