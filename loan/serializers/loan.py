from rest_framework import serializers
from loan.models import Customer
from loan.models.loan import Loan
from .customer import CustomerDescriptonSerializer


from datetime import date
from dateutil.relativedelta import relativedelta  # more accurate for adding months
from loan.services import check_loan_eligibility


class LoanRequestSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    loan_amount = serializers.FloatField()
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()

    def create(self, validated_data):
        customer = validated_data["customer_id"]
        amount = float(validated_data["loan_amount"])
        rate = float(validated_data["interest_rate"])
        tenure = validated_data["tenure"]

        check_status = check_loan_eligibility(customer, amount, rate, tenure)
        is_eligible = check_status["approval"]

        if not is_eligible:
            raise serializers.ValidationError(check_status["message"])
        corrected_rate = float(check_status["corrected_interest_rate"])

        rate = corrected_rate

        # Calculate monthly EMI: simple interest EMI formula
        # EMI = [P * R * (1+R)^N] / [(1+R)^N - 1]
        P = amount
        R = rate / 100 / 12  # monthly interest rate
        N = 60  # 5 years

        if R == 0:
            emi = P / N
        else:
            emi = P * R * ((1 + R) ** N) / (((1 + R) ** N) - 1)

        end_date = date.today() + relativedelta(years=5)

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=amount,
            interest_rate=rate,
            tenure=N,
            monthly_payment=round(emi, 2),
            date_of_approval=date.today(),
            end_date=end_date,
        )
        return loan


class LoanResponseSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    loan_id = serializers.PrimaryKeyRelatedField(queryset=Loan.objects.all())
    loan_approved = serializers.BooleanField()
    message = serializers.CharField()  # if not approved.
    monthly_installment = serializers.FloatField()


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            "id",
            "loan_amount",
            "interest_rate",
            "monthly_payment",
            "tenure",
        )


class LoanWithCustomerSerializer(LoanSerializer):
    customer = CustomerDescriptonSerializer(read_only=True)

    class Meta(LoanSerializer.Meta):
        fields = LoanSerializer.Meta.fields + (
            "customer",
        )  # no need to add 'customer'; already part of fields="__all__"


class LoanListSerializer(serializers.Serializer):
    loans = LoanSerializer(many=True)


class LoanImportSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    date_of_approval = serializers.DateField(
        input_formats=["%d/%m/%Y"],
    )
    end_date = serializers.DateField(
        input_formats=["%d/%m/%Y"],
    )

    class Meta:
        model = Loan
        fields = "__all__"

    pass
