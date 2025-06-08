from django.urls import path
from loan.views import RegisterView, CheckEligibilityView
from loan.views.loan import CreateLoanView, ListLoansView, ViewLoanView


# change.
urlpatterns = [
    path("register", RegisterView.as_view(), name="register-user"),
    path("check-eligibility", CheckEligibilityView.as_view(), name="check-eligibility"),
    path("create-loan", CreateLoanView.as_view(), name="create-loan"),
    path("view-loan/<int:loan_id>", ViewLoanView.as_view(), name="view-loan"),
    path("view-loans/<int:customer_id>", ListLoansView.as_view(), name="view-loans"),
]
