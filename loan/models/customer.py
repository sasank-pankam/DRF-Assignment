from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Customer ID, int
# First Name, str
# Last Name, str
# Age, int
# Phone Number, str
# Monthly Salary, int
# Approved Limit, int


class Customer(models.Model):
    id = models.AutoField(primary_key=True)  # eventhough django creates
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    phone_number = models.PositiveBigIntegerField(
        validators=[
            MinValueValidator(1000000000),
            MaxValueValidator(9999999999),  # indian numbers
        ],  # less than 10 digits
        unique=True,
    )
    monthly_income = models.PositiveIntegerField()
    approved_limit = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"
