from rest_framework import serializers
from .models import Discount
from user.models import User

class FavoriteDiscountSerializer(serializers.Serializer):
    discount_id = serializers.IntegerField()

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    fav_discounts = DiscountSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'mobile_phone', 'fav_discounts']