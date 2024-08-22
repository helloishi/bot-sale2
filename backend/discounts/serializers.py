from rest_framework import serializers
from .models import Discount
from user.models import User

class FavoriteDiscountSerializer(serializers.Serializer):
    discount_id = serializers.IntegerField()

class DiscountSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    place_type_display = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = ['id', 'place', 'image', 'description', 'address_txt', 'start_date', 'end_date', 'place_type', 'is_active', 'is_favorite', 'place_type_display']

    def get_is_favorite(self, obj):
        user = self.context.get('user')
        if user:
            return obj in user.fav_discounts.all()
        return False

    def get_place_type_display(self, obj):
        return obj.get_place_type_display()

class UserSerializer(serializers.ModelSerializer):
    fav_discounts = DiscountSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'mobile_phone', 'fav_discounts']