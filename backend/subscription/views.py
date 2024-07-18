from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Subscription
from user.models import User
from .serializers import SubscriptionSerializer

class SubscriptionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class SubscriptionCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        data = request.data.copy()
        data['client'] = user.id
        data['end_date'] = datetime.now().date() + relativedelta(months=1)

        serializer = SubscriptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActiveSubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        today = datetime.now().date()

        return Subscription.objects.filter(
            end_date__gt=today,
            stopped=False
        )

class CheckActiveSubscriptionView(APIView):
    def get(self, request, username, *args, **kwargs):
        today = datetime.now().date()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        has_active_subscription = Subscription.objects.filter(
            client=user,
            end_date__gt=today,
            stopped=False
        ).exists()

        return Response({"has_active_subscription": has_active_subscription})

class SubscriptionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
