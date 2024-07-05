from django.urls import path
from .views import SubscriptionListCreateAPIView, SubscriptionDetailAPIView

urlpatterns = [
    path('subscriptions/', SubscriptionListCreateAPIView.as_view(), name='subscription_list_create'),
    path('subscriptions/<int:pk>/', SubscriptionDetailAPIView.as_view(), name='subscription_detail'),
]
