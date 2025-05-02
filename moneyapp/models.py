# updated models.py

from django.db import models
from django.db.models import UniqueConstraint

class Member(models.Model):
    ROLE_CHOICES = [('Teaching', 'Teaching Staff'), ('Non-Teaching', 'Non-Teaching Staff')]
    name            = models.CharField(max_length=100)
    member_id       = models.CharField(max_length=50, unique=True)
    department      = models.CharField(max_length=100, blank=True)
    designation     = models.CharField(max_length=100, blank=True)
    mob             = models.BigIntegerField()
    email           = models.EmailField()
    dob             = models.DateField()
    doj             = models.DateField()
    doj_service     = models.DateField()
    maximum_period  = models.IntegerField()
    max_loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    city            = models.CharField(max_length=100)
    pincode         = models.CharField(max_length=10)
    role            = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Non-Teaching')
    has_loan        = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Loan(models.Model):
    member               = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='loans')
    loan_no              = models.CharField(max_length=50, unique=True)
    disp_date            = models.DateField()
    sanctioned_amount    = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate        = models.DecimalField(max_digits=5, decimal_places=2)
    repayment_start_date = models.DateField()
    repayment_period     = models.IntegerField()  # in months
    monthly_repayment    = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid          = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    amount_received      = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Loan {self.loan_no} for {self.member.name}"

class LoanRepayment(models.Model):
    member               = models.ForeignKey(Member, on_delete=models.CASCADE)
    repayment_number     = models.PositiveIntegerField()   # sequential number per member
    repayment_date       = models.DateField()
    interest_paid        = models.DecimalField(max_digits=10, decimal_places=2)
    principal_paid       = models.DecimalField(max_digits=10, decimal_places=2)
    total_payment        = models.DecimalField(max_digits=10, decimal_places=2)
    outstanding_balance  = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('member', 'repayment_number')
        constraints = [
            models.UniqueConstraint(fields=['member', 'repayment_number'], name='unique_member_repayment')
        ]

    def __str__(self):
        return f"{self.member.name} – Repayment {self.repayment_number}"
