from django.urls import path
from .views import *

urlpatterns = [
    path('', SubscriptionListCreateAPIView.as_view(), name='subscription_list_create'),
    #path('<int:pk>/', SubscriptionDetailAPIView.as_view(), name='subscription_detail'),
    path('active/', ActiveSubscriptionListView.as_view(), name='active-subscription-list'),
    path('check/<str:username>/', CheckActiveSubscriptionView.as_view(), name='check-active-subscription'),
    path('sub-info/<str:username>/', GetInfoOnSubscription.as_view(), name='subscription-info'),
    path('create/', SubscriptionCreateAPIView.as_view(), name='create-subscription-view'),
    path('stop-subscriptions/', StopUserSubscriptionsView.as_view(), name='stop-subscriptions'),
    path('accept-payment/', AcceptPayment.as_view(), name='accept-payment'),
    path('create-payment-token/', PayForSubscriptionView.as_view(), name='create-payment-token'),
]
