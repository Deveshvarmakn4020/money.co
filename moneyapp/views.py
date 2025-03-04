from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import MemberForm
from .models import Member
from .forms import LoginForm
# home/views.py
from django.shortcuts import render


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')  # Redirect to dashboard after login
#         else:
#             error = "Invalid username or password."
#             return render(request, 'templates/login.html', {'error': error})
#     return render(request, 'login.html')

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

def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})  # Add the class here

def loan_information(request):
    members = Member.objects.filter(has_loan = True )
    return render(request, 'loan.html', {'members': members})


def home(request):
    return render(request, 'home.html')

def loan(request):
    return render(request, 'loan.html')

def members_list(request):
    members = Member.objects.all()  # Retrieve all members
    return render(request, 'members.html', {'members': members})


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
    # Filter teaching staff who have a loan
    teaching_members = Member.objects.filter(role='Teaching', has_loan=True)
    return render(request, 'moneyapp/teaching_staff.html', {'members': teaching_members})



def non_teaching_staff(request):
    # Filter non-teaching staff who have a loan
    non_teaching_members = Member.objects.filter(role='Non-Teaching', has_loan=True)
    return render(request, 'moneyapp/non_teaching_staff.html', {'members': non_teaching_members})

def detail_members(request,  member_id):
    member = get_object_or_404(Member, id=member_id)
    return render(request, 'detail_members.html', {'member': member})