from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import transaction
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

# Home View
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
    return render(request, 'teaching_staff.html', {'members': members})

# Non-Teaching Staff View
def non_teaching_staff(request):
    members = Member.objects.filter(role='Non-Teaching', has_loan=True)
    return render(request, 'non_teaching_staff.html', {'members': members})

# Member Detail View
def detail_members(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    num_repayments = LoanRepayment.objects.filter(member=member).count()
    return render(request, 'detail_members.html', {'member': member, 'num_repayments': num_repayments})

# Loan Repayment View
def loan_repayment(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        try:
            repayment_date = request.POST.get('repayment_date')
            principal_paid = Decimal(request.POST.get('principal_paid', 0))
            if principal_paid <= 0:
                messages.error(request, "Principal amount must be greater than 0.")
                return redirect('loan_repayment', member_id=member_id)
            if principal_paid > member.max_loan_amount:
                messages.error(request, "Principal amount cannot exceed outstanding balance.")
                return redirect('loan_repayment', member_id=member_id)

            # Calculate interest and total
            interest_paid = round(member.max_loan_amount * Decimal('0.009583'), 2)
            total_payment = interest_paid + principal_paid

            # Determine repayment_number and outstanding_balance
            repayment_count = LoanRepayment.objects.filter(member=member).count()
            new_repayment_number = repayment_count + 1
            new_outstanding = member.max_loan_amount - principal_paid

            # Create repayment record and update member in one transaction
            with transaction.atomic():
                LoanRepayment.objects.create(
                    member=member,
                    repayment_number=new_repayment_number,
                    repayment_date=repayment_date,
                    interest_paid=interest_paid,
                    principal_paid=principal_paid,
                    total_payment=total_payment,
                    outstanding_balance=new_outstanding
                )
                member.max_loan_amount = new_outstanding
                if member.max_loan_amount <= 0:
                    member.has_loan = False
                member.save()

            messages.success(request, f"Repayment of ₹{total_payment} recorded successfully!")
            return redirect('detail_members', member_id=member_id)

        except Exception as e:
            messages.error(request, f"Error processing repayment: {str(e)}")
            return redirect('loan_repayment', member_id=member_id)

    # If GET: prepare form with next repayment number
    if member.max_loan_amount <= 0:
        messages.error(request, "No outstanding loan balance.")
        return redirect('loan')
    repayment_count = LoanRepayment.objects.filter(member=member).count()
    ordinal = lambda n: "%d%s" % (n, {1:"st",2:"nd",3:"rd"}.get(n if n<20 else n%10, "th"))
    repayment_number = f"{ordinal(repayment_count+1)} Repayment"
    interest_amount = round(member.max_loan_amount * Decimal('0.009583'), 2)

    return render(request, 'loan_repayment.html', {
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

# Repayments Loanee List
def repayments(request):
    loanees = Member.objects.filter(loanrepayment__isnull=False).distinct()
    return render(request, 'repayment_loanee_list.html', {'loanees': loanees})

# Detailed Repayment View per Loanee
def repayment_details(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    # Order by repayment_number (chronological for that member)
    repayments = LoanRepayment.objects.filter(member=member).order_by('repayment_number')

    total_interest = sum(r.interest_paid for r in repayments)
    total_principal = sum(r.principal_paid for r in repayments)
    final_balance = member.max_loan_amount

    return render(request, 'repayment_detail.html', {
        'member': member,
        'repayments': repayments,
        'total_interest': total_interest,
        'total_principal': total_principal,
        'final_balance': final_balance
    })