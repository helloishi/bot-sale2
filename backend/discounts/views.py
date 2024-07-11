from rest_framework import generics, status
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User
from .models import Discount
from .serializers import DiscountSerializer, AddFavoriteDiscountSerializer
from .filters import DiscountFilter

class AddFavoriteDiscountView(APIView):
    def post(self, request, username, *args, **kwargs):
        serializer = AddFavoriteDiscountSerializer(data=request.data)
        if serializer.is_valid():
            discount_id = serializer.validated_data['discount_id']
            try:
                user = User.objects.get(username=username)
                discount = Discount.objects.get(id=discount_id)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except Discount.DoesNotExist:
                return Response({"detail": "Discount not found."}, status=status.HTTP_404_NOT_FOUND)

            user.fav_discounts.add(discount)
            return Response({"detail": "Discount added to favorites."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiscountListCreateAPIView(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DiscountFilter

class DiscountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
