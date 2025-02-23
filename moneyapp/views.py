from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import MemberForm, LoginForm
from .models import Member

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
    members = Member.objects.all()
    return render(request, 'loan.html', {'members': members})

def home(request):
    return render(request, 'home.html')

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

def teaching_staff(request):
    teaching_members = Member.objects.filter(role='Teaching', has_loan=True)
    return render(request, 'moneyapp/teaching_staff.html', {'members': teaching_members})

def non_teaching_staff(request):
    non_teaching_members = Member.objects.filter(role='Non-Teaching', has_loan=True)
    return render(request, 'moneyapp/non_teaching_staff.html', {'members': non_teaching_members})

def detail_members(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    return render(request, 'detail_members.html', {'member': member})

def next_page(request):
    return render(request, 'next_page.html')

def index(request):
    return render(request, 'index.html')

def loan_application(request):
    return render(request, 'loan_application.html')
