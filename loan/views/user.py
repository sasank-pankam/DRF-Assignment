from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from loan.serializers import (
    CustomerRegisterSerializer,
    LoanRequestSerializer,
    EligibilityResultSerializer,
)
from loan.serializers.customer import CustomerSerializer
from loan.services import check_loan_eligibility


class RegisterView(APIView):
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            response_serializer = CustomerSerializer(customer)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckEligibilityView(APIView):
    def post(self, request):
        serializer = LoanRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            result = check_loan_eligibility(
                customer=data["customer_id"],
                loan_amount=data["loan_amount"],
                interest_rate=data["interest_rate"],
                tenure=data["tenure"],
            )
            return Response(
                EligibilityResultSerializer(result).data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
