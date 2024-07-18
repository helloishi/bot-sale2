from rest_framework import serializers
from .models import Discount
from user.models import User

class FavoriteDiscountSerializer(serializers.Serializer):
    discount_id = serializers.IntegerField()

class DiscountSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = ['id', 'place', 'image', 'description', 'address_txt', 'start_date', 'end_date', 'place_type', 'is_active', 'is_favorite']

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        return obj in user.fav_discounts.all()

class UserSerializer(serializers.ModelSerializer):
    fav_discounts = DiscountSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'mobile_phone', 'fav_discounts']