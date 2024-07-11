from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    invoice_id = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    account_id = serializers.CharField(max_length=100)
    card_cryptogram_packet = serializers.CharField()
