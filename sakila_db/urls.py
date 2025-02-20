from django.urls import path
from .views import TopRentedFilmsView, FilmView, FilmListView, CustomerListView, CustomerRentalsView, TopActorsView, ActorView

urlpatterns = [
    path('api/films/', FilmListView.as_view(), name='getAllFilms'),
    path('api/films/top/', TopRentedFilmsView.as_view(), name='getTopFilms'),
    path('api/film/<int:filmId>/', FilmView.as_view(), name='getFilm'),
    path('api/actors/top/', TopActorsView.as_view(), name='getTopActors'),
    path('api/actor/<int:actorId>/', ActorView.as_view(), name='getActor'),
    path('api/customers/', CustomerListView.as_view(), name='getAllCustomers'),
    path('api/customer/<int:customerId>/rentals/', CustomerRentalsView.as_view(), name='getCustomerRentals')
]