import csv
from django.db.utils import IntegrityError
from rest_framework import serializers
from loan.serializers import CustomerSerializer, LoanImportSerializer


# 29 rows in the loan section is having duplciate loan id's so ignored them.
CUSTOMER_HEADERS = [
    ("id", int),
    ("first_name", str),
    ("last_name", str),
    ("age", int),
    ("phone_number", int),
    ("monthly_income", int),
    ("approved_limit", int),
]


LOAN_HEADERS = [
    ("customer", int),
    ("id", int),
    ("loan_amount", int),
    ("tenure", int),
    ("interest_rate", float),
    ("monthly_payment", int),
    ("emis_paid_on_time", int),
    ("date_of_approval", str),
    ("end_date", str),
]


def import_data(csv_path, headers, serializer):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header

        success = 0
        failed = 0

        for row in reader:
            if len(row) != len(headers):
                # print(f"Skipping invalid row (wrong length): {row}")
                failed += 1
                continue
            data = {}
            for (name, _type), val in zip(headers, row):
                data[name] = _type(val)

            try:
                obj = serializer(data=data)
                if obj.is_valid():
                    obj.save()
                success += 1
            except serializers.ValidationError:
                # print(f"Validation failed for row {row}: {ve}")
                failed += 1
            except IntegrityError:
                # print(f"Id already exists for row {row}: {ve}")
                failed += 1
            except Exception:
                # print("Cannot upload user, for reason:", e)
                # print(data)
                pass


import_data("./customer_data.csv", CUSTOMER_HEADERS, CustomerSerializer)
import_data("./loan_data.csv", LOAN_HEADERS, LoanImportSerializer)
