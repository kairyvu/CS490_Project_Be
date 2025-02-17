from django.urls import path
from . import views
from .views import TopRentedFilmsView, FilmView

urlpatterns = [
    path('api/films/top/', TopRentedFilmsView.as_view(), name='getTopFilms'),
    path('api/film/<int:filmId>/', FilmView.as_view(), name='getFilm'),
]