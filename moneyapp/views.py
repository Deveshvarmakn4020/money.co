from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import transaction
from .forms import MemberForm, LoginForm, LoanForm
from .models import Member, Loan, LoanRepayment
from decimal import Decimal
from django.db.models import Max, Sum


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


def home(request):
    return render(request, 'home.html')


def register_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MemberForm()
    return render(request, 'register_member.html', {'form': form})


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


def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('loan')


def loan_information(request):
    members = Member.objects.all()
    return render(request, 'loan.html', {'members': members})


def teaching_staff(request):
    members = Member.objects.filter(role='Teaching', has_loan=True)
    return render(request, 'teaching_staff.html', {'members': members})


def non_teaching_staff(request):
    members = Member.objects.filter(role='Non-Teaching', has_loan=True)
    return render(request, 'non_teaching_staff.html', {'members': members})


def detail_members(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    num_repayments = LoanRepayment.objects.filter(member=member).count()
    return render(request, 'detail_members.html', {
        'member': member,
        'num_repayments': num_repayments
    })


# ✅ UPDATED Loan Repayment (Dropdown logic added)
def loan_repayment(request, member_id):

    # Default member (page opened for this member)
    default_member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        try:
            # 🔥 NEW: Check dropdown selection
            selected_member_id = request.POST.get('selected_member')

            if selected_member_id:
                member = get_object_or_404(Member, id=selected_member_id)
            else:
                member = default_member

            repayment_date = request.POST.get('repayment_date')
            principal_paid = Decimal(request.POST.get('principal_paid', 0))
            rd_amount = Decimal(request.POST.get('rd_amount', 0))

            if principal_paid <= 0:
                messages.error(request, "Principal amount must be greater than 0.")
                return redirect('loan_repayment', member_id=default_member.id)

            if principal_paid > member.max_loan_amount:
                messages.error(request, "Principal amount cannot exceed outstanding balance.")
                return redirect('loan_repayment', member_id=default_member.id)

            interest_paid = round(member.max_loan_amount * Decimal('0.009583'), 2)
            total_payment = interest_paid + principal_paid + rd_amount

            repayment_count = LoanRepayment.objects.filter(member=member).count()
            new_outstanding = member.max_loan_amount - principal_paid

            with transaction.atomic():
                LoanRepayment.objects.create(
                    member=member,
                    repayment_number=repayment_count + 1,
                    repayment_date=repayment_date,
                    interest_paid=interest_paid,
                    principal_paid=principal_paid,
                    rd_amount=rd_amount,
                    total_payment=total_payment,
                    outstanding_balance=new_outstanding
                )

                member.max_loan_amount = new_outstanding
                if member.max_loan_amount <= 0:
                    member.has_loan = False
                member.save()

            messages.success(request, "Repayment recorded successfully!")

            # 🔥 Redirect to correct member detail
            return redirect('repayment_details', member_id=member.id)

        except Exception as e:
            messages.error(request, str(e))
            return redirect('loan_repayment', member_id=default_member.id)

    # GET request logic (unchanged but cleaned)
    interest_amount = round(default_member.max_loan_amount * Decimal('0.009583'), 2)
    repayment_count = LoanRepayment.objects.filter(member=default_member).count()
    repayment_number = repayment_count + 1

    # 🔥 NEW: send all members with loan for dropdown
    all_members = Member.objects.filter(has_loan=True)

    return render(request, 'loan_repayment.html', {
        'member': default_member,
        'interest_amount': interest_amount,
        'repayment_number': repayment_number,
        'all_members': all_members
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


def repayments(request):
    loanees = Member.objects.filter(loanrepayment__isnull=False).distinct()
    return render(request, 'repayment_loanee_list.html', {'loanees': loanees})


def repayment_details(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    repayments = LoanRepayment.objects.filter(member=member).order_by('repayment_number')

    totals = repayments.aggregate(
        total_interest=Sum('interest_paid'),
        total_principal=Sum('principal_paid'),
        total_rd=Sum('rd_amount')
    )

    return render(request, 'repayment_detail.html', {
        'member': member,
        'repayments': repayments,
        'total_interest': totals['total_interest'] or 0,
        'total_principal': totals['total_principal'] or 0,
        'total_rd': totals['total_rd'] or 0,
        'final_balance': member.max_loan_amount
    })


def paid_off_list(request):
    latest = LoanRepayment.objects.values('member').annotate(latest_id=Max('id'))
    latest_ids = [i['latest_id'] for i in latest]
    paid_off = LoanRepayment.objects.filter(id__in=latest_ids, outstanding_balance=0)
    return render(request, 'paid_off_list.html', {'paid_off_loanees': paid_off})


def view_paid_off_details(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    repayments = LoanRepayment.objects.filter(member=member)

    totals = repayments.aggregate(
        total_interest=Sum('interest_paid'),
        total_principal=Sum('principal_paid'),
        total_rd=Sum('rd_amount')
    )

    return render(request, 'paid_off_detail.html', {
        'member': member,
        'repayments': repayments,
        'total_interest': totals['total_interest'] or 0,
        'total_principal': totals['total_principal'] or 0,
        'total_rd': totals['total_rd'] or 0,
        'final_balance': member.max_loan_amount
    })


def paid_off_loanees(request):
    members = Member.objects.filter(max_loan_amount=0)
    return render(request, 'paid_off.html', {'members': members})
