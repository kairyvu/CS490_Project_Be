from django.shortcuts import render
from django.http import JsonResponse
from sakila_db.services import getTopRentedFilms

# Create your views here.

def getTopFilms(request):
    filmList = getTopRentedFilms()
    return JsonResponse(list(filmList), safe=False)