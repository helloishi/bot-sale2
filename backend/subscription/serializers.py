from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = Subscription
        fields = '__all__'
