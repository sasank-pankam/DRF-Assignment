from loan.models import Loan, Customer
from rest_framework import status
from .__common import AuthenticatedTestCase


class CommonSetup(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        customer_data = {
            "first_name": "Annamarie",
            "last_name": "Asensio",
            "age": 43,
            "phone_number": 9772698915,
            "monthly_income": 65000,
            "approved_limit": 4700000,
        }
        self.customer = Customer.objects.create(id=1, **customer_data)

        loans = [
            {
                "loan_amount": 600000,
                "tenure": 90,
                "interest_rate": 16.14,
                "monthly_payment": 19001,
                "emis_paid_on_time": 56,
                "date_of_approval": "2018-02-16",
                "end_date": "2025-08-16",
            },
            {
                "loan_amount": 100000,
                "tenure": 9,
                "interest_rate": 9.16,
                "monthly_payment": 11111,
                "emis_paid_on_time": 7,
                "date_of_approval": "2022-10-11",
                "end_date": "2023-07-11",
            },
            {
                "loan_amount": 400000,
                "tenure": 105,
                "interest_rate": 15.42,
                "monthly_payment": 11998,
                "emis_paid_on_time": 81,
                "date_of_approval": "2021-01-25",
                "end_date": "2029-10-25",
            },
            {
                "loan_amount": 300000,
                "tenure": 27,
                "interest_rate": 11.48,
                "monthly_payment": 13809,
                "emis_paid_on_time": 14,
                "date_of_approval": "2018-08-19",
                "end_date": "2020-11-19",
            },
            {
                "loan_amount": 200000,
                "tenure": 42,
                "interest_rate": 12.65,
                "monthly_payment": 6807,
                "emis_paid_on_time": 24,
                "date_of_approval": "2019-02-06",
                "end_date": "2022-08-06",
            },
        ]

        for i, l in enumerate(loans, 1):
            Loan.objects.create(
                id=i,
                customer=self.customer,
                **l,
            )


class LoanCreateViewTest(CommonSetup):
    def setUp(self):
        super().setUp()
        self.url = "/api/create-loan"

    def test_create_loan(self):
        payloads = [
            (
                {
                    "customer_id": 1,
                    "loan_amount": 10000,
                    "tenure": 12,
                    "interest_rate": 10.0,
                },
                {"status": status.HTTP_201_CREATED},
            ),
        ]
        for payload, res in payloads:
            response = self.client.post(self.url, payload, format="json")
            self.assertEqual(response.status_code, res["status"])


class LoanViewTest(CommonSetup):
    def setUp(self):
        super().setUp()
        self.url = "/api/view-loan"

    def test_view_loan(self):
        payloads = [
            (
                1,
                {
                    "id": 1,
                    "loan_amount": 600000,
                    "interest_rate": "16.14",
                    "monthly_payment": "19001.00",
                    "tenure": 90,
                    "customer": {
                        "id": 1,
                        "first_name": "Annamarie",
                        "last_name": "Asensio",
                        "age": 43,
                        "phone_number": 9772698915,
                    },
                },
            ),
            (
                2,
                {
                    "id": 2,
                    "loan_amount": 100000,
                    "interest_rate": "9.16",
                    "monthly_payment": "11111.00",
                    "tenure": 9,
                    "customer": {
                        "id": 1,
                        "first_name": "Annamarie",
                        "last_name": "Asensio",
                        "age": 43,
                        "phone_number": 9772698915,
                    },
                },
            ),
        ]
        for payload, res in payloads:
            response = self.client.get(self.url + f"/{payload}")
            self.assertEqual(response.data, res)


class LoansOfCustomerViewTest(CommonSetup):
    def setUp(self):
        super().setUp()
        self.url = "/api/view-loans"

    def test_view_loan(self):
        payloads = [
            (
                1,
                {
                    "loans": [
                        {
                            "id": 1,
                            "loan_amount": 600000,
                            "tenure": 90,
                            "interest_rate": "16.14",
                            "monthly_payment": "19001.00",
                        },
                        {
                            "id": 2,
                            "loan_amount": 100000,
                            "tenure": 9,
                            "interest_rate": "9.16",
                            "monthly_payment": "11111.00",
                        },
                        {
                            "id": 3,
                            "loan_amount": 400000,
                            "tenure": 105,
                            "interest_rate": "15.42",
                            "monthly_payment": "11998.00",
                        },
                        {
                            "id": 4,
                            "loan_amount": 300000,
                            "tenure": 27,
                            "interest_rate": "11.48",
                            "monthly_payment": "13809.00",
                        },
                        {
                            "id": 5,
                            "loan_amount": 200000,
                            "tenure": 42,
                            "interest_rate": "12.65",
                            "monthly_payment": "6807.00",
                        },
                    ]
                },
            ),
        ]
        for payload, res in payloads:
            response = self.client.get(self.url + f"/{payload}")
            self.assertEqual(response.data, res)


class EligibilityCheckTest(CommonSetup):
    def setUp(self):
        super().setUp()
        self.url = "/api/check-eligibility"

    def test_eligibility(self):
        payloads = [
            (
                {
                    "customer_id": 1,
                    "loan_amount": 10000,
                    "tenure": 20,
                    "interest_rate": 10.0,
                },
                {"status": status.HTTP_202_ACCEPTED},
            ),
            (
                {
                    "customer_id": 1,
                    "loan_amount": 10000,
                    "tenure": 12,
                    "interest_rate": 10.0,
                },
                {"status": status.HTTP_202_ACCEPTED},
            ),
        ]
        for payload, res in payloads:
            response = self.client.post(self.url, payload, format="json")
            self.assertEqual(response.status_code, res["status"])
