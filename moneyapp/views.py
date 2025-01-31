from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
# home/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home/index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('templates/home.html')  # Redirect to dashboard after login
        else:
            error = "Invalid username or password."
            return render(request, 'templates/login.html', {'error': error})
    return render(request, 'login.html')
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