from django.db import models
from django.utils import timezone
from .customer import Customer

# Customer ID,
# Loan ID,
# Loan Amount,
# Tenure,
# Interest Rate,
# Monthly payment,
# EMIs paid on Time,
# Date of Approval,
# End Date


class Loan(models.Model):
    id = models.AutoField(primary_key=True)  # eventhough django creates
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True
    )  # the null is for a record. can handle with some func to add metadata about user instead of linking him.
    loan_amount = models.PositiveIntegerField()
    tenure = models.PositiveIntegerField(help_text="Tenure in months")
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Annual interest rate in %"
    )
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.PositiveIntegerField(default=0)
    date_of_approval = models.DateField(default=timezone.now)
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.id} for Customer {self.customer.id}"
