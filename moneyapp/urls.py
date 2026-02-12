from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Dashboard
    path('home/', views.home, name='home'),

    # Member Management
    path('reg-member/', views.register_member, name='register_member'),
    path('edit-member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),

    # Loan Info
    path('loan/', views.loan_information, name='loan'),
    path('add-loan/<int:member_id>/', views.add_loan, name='add_loan'),

    # Staff Filters
    path('teaching_staff/', views.teaching_staff, name='teaching_staff'),
    path('non_teaching_staff/', views.non_teaching_staff, name='non_teaching_staff'),

    # Member Details
    path('details/<int:member_id>/', views.detail_members, name='detail_members'),

    # Repayment
    path('loan-repayment/<int:member_id>/', views.loan_repayment, name='loan_repayment'),
    path('repayments/', views.repayments, name='repayment_loanee_list'),
    path('repayments/<int:member_id>/', views.repayment_details, name='repayment_detail'),
    path('paid_off/', views.paid_off_list, name='paid_off_list'),
    path('paid_off/view/<int:member_id>/', views.view_paid_off_details, name='view_paid_off_details'),  # placeholder
    path('paid-off/', views.paid_off_loanees, name='paid_off_loanees'),
    path('reports/monthly/', views.monthly_report, name='monthly_report'),
    path('reports/monthly/pdf/', views.monthly_report_pdf, name='monthly_report_pdf'),

]
