from rest_framework import serializers
from .models import Discount

class AddFavoriteDiscountSerializer(serializers.Serializer):
    discount_id = serializers.IntegerField()

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
