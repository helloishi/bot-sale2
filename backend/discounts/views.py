from rest_framework import generics, status
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.models import User
from .models import Discount
from .serializers import *
from .filters import DiscountFilter
from tools import validate_username

class AddFavoriteDiscountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username, *args, **kwargs):
        serializer = FavoriteDiscountSerializer(data=request.data)
        if serializer.is_valid():
            discount_id = serializer.validated_data['discount_id']
            try:
                username = validate_username(username)
                user = User.objects.get(username=username)
                discount = Discount.objects.get(id=discount_id)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except Discount.DoesNotExist:
                return Response({"detail": "Discount not found."}, status=status.HTTP_404_NOT_FOUND)

            user.fav_discounts.add(discount)
            return Response({"detail": "Discount added to favorites."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveFavoriteDiscountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username, *args, **kwargs):
        serializer = FavoriteDiscountSerializer(data=request.data)
        if serializer.is_valid():
            discount_id = serializer.validated_data['discount_id']
            try:
                username = validate_username(username)
                user = User.objects.get(username=username)
                discount = Discount.objects.get(id=discount_id)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except Discount.DoesNotExist:
                return Response({"detail": "Discount not found."}, status=status.HTTP_404_NOT_FOUND)

            if discount in user.fav_discounts.all():
                user.fav_discounts.remove(discount)
                return Response({"detail": "Discount removed from favorites."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Discount not in favorites."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFavoriteDiscountsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        user = request.user
        favorite_discounts = user.fav_discounts.all()
        serializer = DiscountSerializer(favorite_discounts, many=True)

        return Response(serializer.data)

class DiscountViewByPlaceType(APIView):
    def get(self, request):
        place_type = request.query_params.get('place_type', None)
        filterset = DiscountFilter(request.GET, queryset=Discount.objects.all())

        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        if place_type:
            discounts = filterset.qs.filter(place_type=place_type)
        else:
            discounts = filterset.qs

        serializer = DiscountSerializer(discounts, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class DiscountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
