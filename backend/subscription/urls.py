from django.urls import path
from .views import *

urlpatterns = [
    path('', SubscriptionListCreateAPIView.as_view(), name='subscription_list_create'),
    path('<int:pk>/', SubscriptionDetailAPIView.as_view(), name='subscription_detail'),
    path('active/', ActiveSubscriptionListView.as_view(), name='active-subscription-list'),
    path('check/<str:username>/', CheckActiveSubscriptionView.as_view(), name='check-active-subscription'),
]
