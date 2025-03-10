from django.contrib import admin
from .models import Member, Loan

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'member_id', 'department', 'mob', 'has_loan']
    search_fields = ['name', 'member_id']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['loan_no', 'member', 'sanctioned_amount', 'disp_date', 'repayment_start_date']
    search_fields = ['loan_no', 'member__name']