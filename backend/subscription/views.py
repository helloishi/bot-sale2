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
from tools import validate_username, fetch_payments_from_cloud_payments, stop_cloud_payments_recurrent
from payment import *

class SubscriptionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class GetPaymentTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = YooKassaPayment.get_confirmation_token()
        
        return Response({
            "confirmation_token": token
        })

class GetPaymentLinkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        link = token = YooKassaPayment.get_confirmation_link()
        
        return Response({
            "confirmation_link": link
        })

class StopUserSubscriptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        email = user.email
        subscriptions = Subscription.objects.filter(client=user, stopped=False)
        updated_count = subscriptions.update(stopped=True)

        #subscription_ids = fetch_payments_from_cloud_payments(email)
        #stop_cloud_payments_recurrent(subscription_ids, email)
        
        return Response({"updated_count": updated_count}, status=status.HTTP_200_OK)

class AcceptPayment(APIView):
    def post(self, request):
        return Response(request.body, status=status.HTTP_200_OK)  

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
        end_date = latest_subscription.end_date.strftime("%d.%m.%Y")

        return Response({
            "next_payment": end_date,
        }, status=status.HTTP_200_OK)



class SubscriptionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
