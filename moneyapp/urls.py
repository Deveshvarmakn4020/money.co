from django.urls import path
from . import views
from .views import register_member
from .views import home

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', home, name='home'),
    path('reg-member/', register_member, name='register_member'),
    # path('loan/', views.loan_application, name='loan_application'),
    path('next/', views.next_page, name='next_page'),
    path('', views.index, name='index'),  # Home page with buttons
    path('teaching_staff/', views.teaching_staff, name='teaching_staff'),
    path('non_teaching_staff/', views.non_teaching_staff, name='non_teaching_staff'),
    path('loan/', views.loan, name='loan'),
    # path('loan_application/', views.loan_application, name='loan_application'),  
    
]