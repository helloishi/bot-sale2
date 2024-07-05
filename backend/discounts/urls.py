from django.urls import path
from .views import DiscountListCreateAPIView, DiscountDetailAPIView

urlpatterns = [
    path('discounts/', DiscountListCreateAPIView.as_view(), name='discount_list_create'),
    path('discounts/<int:pk>/', DiscountDetailAPIView.as_view(), name='discount_detail'),
]
