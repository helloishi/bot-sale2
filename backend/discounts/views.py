from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Place, Discount
from .serializers import PlaceSerializer, DiscountSerializer


class PlaceListCreateAPIView(APIView):
    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaceDetailAPIView(APIView):
    def get(self, request):
        place = self.get_object(pk)
        serializer = PlaceSerializer(place)

        return Response(serializer.data)


class DiscountListCreateAPIView(APIView):
    def get(self, request):
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)

        return Response(serializer.data)


class DiscountDetailAPIView(APIView):
    def get(self, request, pk):
        discount = self.get_object(pk)
        serializer = DiscountSerializer(discount)
