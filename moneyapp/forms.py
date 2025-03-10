from django import forms
from .models import Member, Loan
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'  # Includes all fields from the model
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'doj': forms.DateInput(attrs={'type': 'date'}),
            'doj_service': forms.DateInput(attrs={'type': 'date'})
        }

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['loan_no', 'disp_date', 'sanctioned_amount', 'interest_rate', 'repayment_start_date', 'repayment_period', 'monthly_repayment']
        widgets = {
            'disp_date': forms.DateInput(attrs={'type': 'date'}),
            'repayment_start_date': forms.DateInput(attrs={'type': 'date'}),
        }