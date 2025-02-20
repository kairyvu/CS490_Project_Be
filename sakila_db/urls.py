from django.urls import path
from . import views
from .views import TopRentedFilmsView, FilmView, FilmListView, CustomerListView

urlpatterns = [
    path('api/films/', FilmListView.as_view(), name='getAllFilms'),
    path('api/films/top/', TopRentedFilmsView.as_view(), name='getTopFilms'),
    path('api/film/<int:filmId>/', FilmView.as_view(), name='getFilm'),
    path('api/actors/top/', views.TopActorsView.as_view(), name='getTopActors'),
    path('api/actor/<int:actorId>/', views.ActorView.as_view(), name='getActor'),
    path('api/customers/', CustomerListView.as_view(), name='getAllCustomers'),
]