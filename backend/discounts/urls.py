from django.urls import path
from .views import *

urlpatterns = [
    path('', DiscountListCreateAPIView.as_view(), name='discount_list_create'),
    path('<int:pk>/', DiscountDetailAPIView.as_view(), name='discount_detail'),
    path('<str:username>/add_favorite/', AddFavoriteDiscountView.as_view(), name='add-favorite-discount'),
    path('<str:username>/remove_favorite/', RemoveFavoriteDiscountView.as_view(), name='remove-favorite-discount'),
]

