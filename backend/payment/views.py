import os 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .payments import CloudPayments
from .serializers import PaymentSerializer
import decimal

class ProcessPaymentView(APIView):
     def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = CloudPayments()
            response_data, response_status = payment.create_payment(
                amount=serializer.validated_data['amount'],
                currency=serializer.validated_data['currency'],
                invoice_id=serializer.validated_data['invoice_id'],
                description=serializer.validated_data['description'],
                account_id=serializer.validated_data['account_id'],
                card_cryptogram_packet=serializer.validated_data['card_cryptogram_packet']
            )

            if response_status == status.HTTP_302_FOUND:
                acs_url = response_data["acs_url"]
                pa_req = response_data["pa_req"]
                redirect_url = f"{acs_url}?PaReq={pa_req}"
                return Response({"redirect_url": redirect_url}, status=status.HTTP_302_FOUND)

            return Response(response_data, status=response_status)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)