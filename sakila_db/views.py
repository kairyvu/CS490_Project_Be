from django.shortcuts import render
from django.http import JsonResponse
from sakila_db.services import getFilmDetails, getTopRentedFilms

# Create your views here.

def getTopFilms(request, limit=5):
    filmList = getTopRentedFilms(limit)
    return JsonResponse({
        "top_films": filmList,
    })

def getFilm(request, filmId):
    filmDetails = getFilmDetails(filmId)
    return JsonResponse({
        "film_details": filmDetails,
    })
