from django.urls import path
from loan.views import ProtectedView


# change.
urlpatterns = [
    path("register", ProtectedView.as_view(), name="token_obtain_pair"),
    path("check-eligibility", ProtectedView.as_view(), name="token_obtain_pair"),
    path("create-loan", ProtectedView.as_view(), name="token_obtain_pair"),
    path("view-loan/<int:loan_id>", ProtectedView.as_view(), name="token_obtain_pair"),
    path(
        "view-loans/<int:customer_id>",
        ProtectedView.as_view(),
        name="token_obtain_pair",
    ),
]
