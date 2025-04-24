from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import MemberForm, LoginForm, LoanForm
from .models import Member, Loan, LoanRepayment
from decimal import Decimal

# Login View
def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid credentials")
    return render(request, 'login.html', {'form': form})

# Home
def home(request):
    return render(request, 'home.html')

# Register Member
def register_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MemberForm()
    return render(request, 'register_member.html', {'form': form})

# Edit Member
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('loan')
    else:
        form = MemberForm(instance=member)
    return render(request, 'edit_member.html', {'form': form})

# Delete Member
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('loan')

# Loan Info (List Members)
def loan_information(request):
    members = Member.objects.all()
    return render(request, 'loan.html', {'members': members})

# Teaching Staff View
def teaching_staff(request):
    members = Member.objects.filter(role='Teaching', has_loan=True)
    return render(request, 'moneyapp/teaching_staff.html', {'members': members})

# Non-Teaching Staff View
def non_teaching_staff(request):
    members = Member.objects.filter(role='Non-Teaching', has_loan=True)
    return render(request, 'moneyapp/non_teaching_staff.html', {'members': members})

# Member Detail View
def detail_members(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    num_repayments = LoanRepayment.objects.filter(member=member).count()
    return render(request, 'detail_members.html', {'member': member, 'num_repayments': num_repayments})

# Loan Repayment View
def loan_repayment(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    loan_balance = Decimal(member.max_loan_amount)
    if loan_balance <= 0:
        messages.error(request, "No outstanding loan balance.")
        return redirect('loan')

    interest_rate = Decimal('0.115')
    interest_amount = round(loan_balance * interest_rate, 2)

    # Calculate repayment number
    repayment_count = LoanRepayment.objects.filter(member=member).count()
    suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(repayment_count + 1 if (repayment_count + 1) < 20 else (repayment_count + 1) % 10, 'th')
    repayment_number = f"{repayment_count + 1}{suffix} Repayment"

    return render(request, 'moneyapp/loan_repayment.html', {
        'member': member,
        'interest_amount': interest_amount,
        'repayment_number': repayment_number,
    })

# Add Loan View
def add_loan(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.member = member
            loan.save()
            member.has_loan = True
            member.save()
            return redirect('loan')
    else:
        form = LoanForm()
    return render(request, 'add_loan.html', {'form': form, 'member': member})
