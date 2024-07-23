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
from tools import validate_username

class SubscriptionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class StopUserSubscriptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        subscriptions = Subscription.objects.filter(client=user, stopped=False)
        updated_count = subscriptions.update(stopped=True)
        return Response({"updated_count": updated_count}, status=status.HTTP_200_OK)

class AcceptPayment(APIView):
    def post(self, request):
        print(request)  

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
            username = validate_username(username)
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        has_active_subscription = Subscription.objects.filter(
            client=user,
            end_date__gt=today,
            stopped=False
        ).exists()

        return Response({"has_active_subscription": has_active_subscription})

class GetInfoOnSubscription(APIView):
    def get(self, request, username, *args, **kwargs):
        today = datetime.now().date()

        try:
            username = validate_username(username)
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        subscriptions = Subscription.objects.filter(
            client=user, 
            end_date__gt=today,
            stopped=False
        ).order_by("-end_date")

        if not subscriptions:
            return Response({"detail": "Subscriptions not found."}, status=status.HTTP_404_NOT_FOUND)

        latest_subscription = subscriptions.first()

        return Response({
            "next_payment": str(latest_subscription.end_date),
            "start_date": str(latest_subscription.start_date)
        }, status=status.HTTP_200_OK)



class SubscriptionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
