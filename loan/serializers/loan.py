from rest_framework import serializers
from loan.models import Customer


class LoanRegisterSerializer(serializers.ModelSerializer):
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


class LoanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class LoanListSerializer(serializers.Serializer):
    loans = LoanDetailSerializer(many=True)
