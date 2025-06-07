from rest_framework import serializers
from loan.models import Customer


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "age", "phone_number", "monthly_salary"]

    def create(self, validated_data):
        salary = validated_data["monthly_salary"]
        approved_limit = self.calculate_approved_limit(salary)
        validated_data["approved_limit"] = approved_limit
        return super().create(validated_data)

    def calculate_approved_limit(self, salary):
        return min(salary * 20, 1000000)


class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


# for short info
class CustomerSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name"]
