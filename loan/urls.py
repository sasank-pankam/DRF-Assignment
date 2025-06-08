from django.urls import path
from loan.views import RegisterView, CheckEligibilityView
from loan.views.loan import CreateLoanView, ListLoansView, ViewLoanView


# change.
urlpatterns = [
    path("register", RegisterView.as_view(), name="register_loan"),
    path("check-eligibility", CheckEligibilityView.as_view(), name="check_eligibility"),
    path("create-loan", CreateLoanView.as_view(), name="create_loan"),
    path("view-loan/<int:loan_id>", ViewLoanView.as_view(), name="view_loan"),
    path("view-loans/<int:customer_id>", ListLoansView.as_view(), name="view_loans"),
]
