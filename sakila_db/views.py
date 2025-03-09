from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import getActorDetails, getFilmDetails, getTopActors, getTopRentedFilms, getAllFilms, getAllCustomers, getCustomerRentalHistory
from .services import update_customer_info 
from .serializers import UpdateCustomerSerializer
# Create your views here.

class FilmListView(APIView):
    def get(self, request):
        filmList = getAllFilms()
        return Response(filmList, status=status.HTTP_200_OK)
    
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

class CustomerListView(APIView):
    def get(self, request):
        customerList = getAllCustomers()
        return Response(customerList, status=status.HTTP_200_OK)
    
class CustomerRentalsView(APIView):
    def get(self, request, customerId):
        customerRentals = getCustomerRentalHistory(customerId)
        return Response(customerRentals, status=status.HTTP_200_OK)

class UpdateCustomerView(APIView):
    def put(self, request):
        serializer = UpdateCustomerSerializer(data=request.data)

        if serializer.is_valid():
            customer_data = serializer.validated_data
            result = update_customer_info(customer_data)

            if 'error' in result:
                return Response({"message": result["error"]}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(result, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        {
    "customer_id": 1,
    "first_name": "MARY111",
    "last_name": "SMITH",
    "email": "MARY.SMITH@sakilacustomer.org",
    "address": "1913 Hanoi Way",
    "district": "Nagasaki",
    "city": "Sasebo",
    "country": "Japan",
    "phone": "28303384290"
}