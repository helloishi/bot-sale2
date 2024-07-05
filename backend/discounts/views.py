from rest_framework import generics
from django_filters import rest_framework as filters
from .models import Discount
from .serializers import DiscountSerializer
from .filters import DiscountFilter

class DiscountListCreateAPIView(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DiscountFilter

class DiscountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
