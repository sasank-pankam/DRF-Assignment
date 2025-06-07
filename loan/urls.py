from django.urls import path
from loan.views import ProtectedView


# change.
urlpatterns = [
    path("register", ProtectedView.as_view(), name="register_loan"),
    path("check-eligibility", ProtectedView.as_view(), name="check_eligibility"),
    path("create-loan", ProtectedView.as_view(), name="create_loan"),
    path("view-loan/<int:loan_id>", ProtectedView.as_view(), name="view_loan"),
    path(
        "view-loans/<int:customer_id>",
        ProtectedView.as_view(),
        name="view_loans",
    ),
]
