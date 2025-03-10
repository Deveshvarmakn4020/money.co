from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import MemberForm, LoginForm, LoanForm
from .models import Member, Loan
from decimal import Decimal

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

def register_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MemberForm()

    return render(request, 'register_member.html', {'form': form})

def loan_information(request):
    members = Member.objects.all()  # Retrieve all registered members
    return render(request, 'loan.html', {'members': members})

def home(request):
    return render(request, 'home.html')

def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('loan')  # Redirect to loan page after editing
    else:
        form = MemberForm(instance=member)
    return render(request, 'edit_member.html', {'form': form})

def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('loan')  # Redirect to loan page after deletion

def teaching_staff(request):
    teaching_members = Member.objects.filter(role='Teaching', has_loan=True)
    return render(request, 'moneyapp/teaching_staff.html', {'members': teaching_members})

def non_teaching_staff(request):
    non_teaching_members = Member.objects.filter(role='Non-Teaching', has_loan=True)
    return render(request, 'moneyapp/non_teaching_staff.html', {'members': non_teaching_members})

def detail_members(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    return render(request, 'detail_members.html', {'member': member})

def loan_repayment(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    
    # Fetch loan balance from member model
    loan_balance = Decimal(member.max_loan_amount)  # Ensure it's Decimal

    if loan_balance <= 0:
        messages.error(request, "No outstanding loan balance.")
        return redirect('loan')

    # Calculate interest
    interest_rate = Decimal('0.115')  # 11.5% interest
    interest_amount = loan_balance * interest_rate  # Now both are Decimal

    return render(request, 'moneyapp/loan_repayment.html', {
        'member': member,
        'interest_amount': round(interest_amount, 2)  # Round to 2 decimal places
    })

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