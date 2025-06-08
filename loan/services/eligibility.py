from datetime import date
from loan.models import Loan
from decimal import Decimal, ROUND_HALF_UP


def calculate_credit_score(customer):
    loans = Loan.objects.filter(customer=customer)
    current_year = date.today().year

    # 1. Check total of current loans (still active)
    active_loans = loans.filter(end_date__gte=date.today())
    total_active_loan_amount = sum(l.loan_amount for l in active_loans)

    if total_active_loan_amount > customer.approved_limit:
        return 0

    score = 0
    score += loans.filter(emis_paid_on_time=True).count() * 5  # i. On-time payment
    score += len(loans) * 2  # ii. Number of loans
    score += (
        loans.filter(date_of_approval__year=current_year).count() * 3
    )  # iii. Current year
    score += int(sum(l.loan_amount for l in loans) / 10000)  # iv. Volume (scaled)

    return min(score, 100)


def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    score = calculate_credit_score(customer)

    monthly_installment = float(loan_amount) / tenure
    monthly_installment = round(monthly_installment, 2)

    current_emis = Loan.objects.filter(customer=customer, end_date__gte=date.today())
    total_existing_emi = sum(l.monthly_payment for l in current_emis)

    if float(total_existing_emi) + monthly_installment > 0.5 * customer.monthly_income:
        return {
            "customer_id": customer,
            "approval": False,
            "interest_rate": interest_rate,
            "corrected_interest_rate": interest_rate,
            "tenure": tenure,
            "monthly_installment": monthly_installment,
            "message": "Rejected: EMIs exceed 50% of monthly salary.",
        }

    rate = float(interest_rate)
    corrected_rate = rate
    approved = False
    message = ""

    message = ""
    if score > 50:
        approved = True
    elif 50 >= score > 30:
        approved = True
        if rate < 12:
            corrected_rate = 12
    elif 30 >= score > 10:
        approved = True
        if rate < 16:
            corrected_rate = 16
    else:
        approved = False
        message = "Rejected: credit score too low."

    return {
        "customer_id": customer,
        "approval": approved,
        "interest_rate": Decimal(str(rate)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        ),
        "corrected_interest_rate": Decimal(str(corrected_rate)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        ),
        "tenure": tenure,
        "monthly_installment": monthly_installment,
        "message": message,
    }
