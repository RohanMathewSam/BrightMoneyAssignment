from decimal import Decimal
from django.db import models
import uuid

# 1. User Table
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aadhar_id = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    credit_score = models.IntegerField(default=300)  # Credit score ranges from 300-900

    def __str__(self):
        return self.name

# 2. Loan Table (Linked to User)
class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_period = models.IntegerField()  # Loan tenure in months
    total_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=[('ACTIVE', 'Active'), ('PAID', 'Paid')], default='ACTIVE')  # ✅ New field

    def save(self, *args, **kwargs):
        # ✅ Ensure values are in Decimal format before calculation
        self.loan_amount = Decimal(self.loan_amount)
        self.interest_rate = Decimal(self.interest_rate)
        self.term_period = int(self.term_period)

        # ✅ Calculate interest and store `total_due`
        interest_amount = (self.loan_amount * self.interest_rate * self.term_period) / Decimal(100)
        self.total_due = self.loan_amount + interest_amount

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan {self.id} for {self.user.name}"

# 3. Payment Table (Linked to Loan)
class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment of ₹{self.amount_paid} for Loan {self.loan.id}"

# 4. BillingCycle Table (Tracks Monthly Billing)
class BillingCycle(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    billing_date = models.DateField()
    due_date = models.DateField()
    min_due = models.DecimalField(max_digits=10, decimal_places=2)
    principal_balance = models.DecimalField(max_digits=10, decimal_places=2)
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Billing for Loan {self.loan.id} on {self.billing_date}"
