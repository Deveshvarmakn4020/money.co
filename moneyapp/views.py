from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import MemberForm
from .models import Member
from .forms import LoginForm
# home/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home/index.html')


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
    members = Member.objects.all()  # Retrieve all registered members
    return render(request, 'loan.html', {'moneyapp_member': members})

def home(request):
    return render(request, 'home.html')

def next_page(request):
    return render(request, 'home/next_page.html')

def index(request):
    return render(request, 'index.html')

def teaching_staff(request):
    return render(request, 'teaching_staff.html')

def non_teaching_staff(request):
    return render(request, 'non_teaching_staff.html')

def loan(request):
    return render(request, 'loan.html')

def loan_application(request):
    return render(request, 'loan_application.html')