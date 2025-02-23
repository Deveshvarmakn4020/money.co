from django.db import models

class Member(models.Model):
    ROLE_CHOICES = [
        ('Teaching', 'Teaching Staff'),
        ('Non-Teaching', 'Non-Teaching Staff'),
    ]
    name = models.CharField(max_length=100)
    member_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    mob = models.BigIntegerField()
    email = models.EmailField()
    dob = models.DateField()
    doj = models.DateField()
    doj_service = models.DateField()
    maximum_period = models.IntegerField()
    max_loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    # Added fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Non-Teaching')
    has_loan = models.BooleanField(default=False)

    # ✅ Change max_eligibity to FloatField
    max_eligibity = models.FloatField(default="NULL")

    def __str__(self):
        return self.name
