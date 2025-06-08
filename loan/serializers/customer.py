from rest_framework import serializers
from loan.models import Customer


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "age", "phone_number", "monthly_income"]

    def create(self, validated_data):
        income = validated_data["monthly_income"]
        approved_limit = self.calculate_approved_limit(income)
        validated_data["approved_limit"] = approved_limit
        return super().create(validated_data)

    def calculate_approved_limit(self, salary):
        raw_limit = 36 * salary
        approved_limit = round(raw_limit / 100000) * 100000  # rounding to newarest lack
        return approved_limit


class CustomerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Customer
        fields = "__all__"


# for short info
class CustomerDescriptonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "phone_number", "age"]


class EligibilityResultSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    approval = serializers.BooleanField()
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    corrected_interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()
    monthly_installment = serializers.FloatField()
