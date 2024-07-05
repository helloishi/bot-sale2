from rest_framework import generics
from .models import Subscription
from .serializers import SubscriptionSerializer

class SubscriptionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class SubscriptionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
