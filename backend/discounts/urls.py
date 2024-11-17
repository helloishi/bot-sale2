from django.urls import path
from .views import *

urlpatterns = [
    path('', DiscountViewByPlaceType.as_view(), name='discount_list_create'),
    path('<int:pk>/', DiscountDetailAPIView.as_view(), name='discount_detail'),
    path('add_favorite/', AddFavoriteDiscountView.as_view(), name='add-favorite-discount'),
    path('remove_favorite/', RemoveFavoriteDiscountView.as_view(), name='remove-favorite-discount'),
    path('get_favorite/', UserFavoriteDiscountsView.as_view(), name='get-favorite-discounts'),
    path('locations/', PlaceView.as_view(), name='location_list_create')
   # path('<str:username>/', DiscountViewByPlaceType.as_view(), name='get-favorite-discounts-with-favorite')
]

