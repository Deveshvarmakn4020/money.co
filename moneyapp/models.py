# moneyapp/models.py
from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    member_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    mob = models.CharField(max_length=15)  # Matches CSV's 'mob' field
    email = models.EmailField()
    dob = models.DateField()
    doj = models.DateField()
    doj_service = models.DateField()
    maximum_period = models.IntegerField()
    max_loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.name