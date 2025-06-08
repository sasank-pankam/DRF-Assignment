from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from loan.serializers import (
    LoanRequestSerializer,
    serializers,
)
from loan.models import Loan
from loan.serializers.loan import (
    LoanListSerializer,
    LoanSerializer,
    LoanWithCustomerSerializer,
)


class CreateLoanView(APIView):
    def post(self, request):
        serializer = LoanRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                loan_request = serializer.save()  # may raise ValidationError
            except serializers.ValidationError as e:
                print("*****1")
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

            response_serializer = LoanSerializer(loan_request)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        print("*****2")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewLoanView(APIView):
    def get(self, request, loan_id):
        try:
            _loan = Loan.objects.select_related("customer").get(id=loan_id)
        except Exception:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LoanWithCustomerSerializer(_loan)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListLoansView(APIView):
    def get(self, request, customer_id):
        try:
            _loans = Loan.objects.filter(customer=customer_id)
        except Exception:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        _serializer = LoanListSerializer({"loans": _loans})
        return Response(_serializer.data, status=status.HTTP_200_OK)
