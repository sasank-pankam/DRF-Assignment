from rest_framework import status
from .__common import AuthenticatedTestCase


class CustomerRegistrViewTest(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.url = "/api/register"

    def test_user_create(self):
        cal_approved_limit = lambda x: round(x / 100000) * 100000
        payloads = [
            (
                {
                    "first_name": "ABC",
                    "last_name": "DEF",
                    "age": 40,
                    "phone_number": 2323232323,
                    "monthly_income": 230000,
                },
                {
                    "id": 1,
                    "approved_limit": cal_approved_limit(230000),
                },
            ),
        ]
        for payload, res in payloads:
            response = self.client.post(self.url, payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, {**payload, **res})
