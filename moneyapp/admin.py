from django.contrib import admin
from .models import Member, Loan, LoanRepayment   # ← import LoanRepayment instead of Repayment

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display  = ['name', 'member_id', 'department', 'mob', 'has_loan']
    search_fields = ['name', 'member_id']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display  = ['loan_no', 'member', 'sanctioned_amount', 'disp_date', 'repayment_start_date']
    search_fields = ['loan_no', 'member__name']

@admin.register(LoanRepayment)  # ← register LoanRepayment here
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'repayment_number', 'repayment_date', 'outstanding_balance')
    ordering     = ('member', 'repayment_number')
