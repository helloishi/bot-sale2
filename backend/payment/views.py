from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .payments import CloudPayments
from .serializers import PaymentSerializer
import decimal

class ProcessPaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            cp = CloudPayments(public_id='your_public_id', api_secret='your_api_secret')
            result = cp.create_payment(
                amount=data['amount'],
                currency=data['currency'],
                invoice_id=data['invoice_id'],
                description=data['description'],
                account_id=data['account_id'],
                card_cryptogram_packet=data['card_cryptogram_packet']
            )

            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)