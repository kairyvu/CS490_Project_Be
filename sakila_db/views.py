from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from sakila_db.services import getActorDetails, getFilmDetails, getTopActors, getTopRentedFilms

# Create your views here.

class TopRentedFilmsView(APIView):
    def get(self, request, limit=5):
        filmList = getTopRentedFilms(limit)
        return Response(filmList, status=status.HTTP_200_OK)

class FilmView(APIView):
    def get(self, request, filmId):
        filmDetails = getFilmDetails(filmId)
        return Response(filmDetails, status=status.HTTP_200_OK)

class TopActorsView(APIView):
    def get(self, request, limit=5):
        actorList = getTopActors(limit)
        return Response(actorList, status=status.HTTP_200_OK)

class ActorView(APIView):
    def get(self, request, actorId):
        actorDetails = getActorDetails(actorId)
        return Response(actorDetails, status=status.HTTP_200_OK)