from django.urls import path
from . import views
from .views import home

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', home, name='home'),
    path('reg-member/', views.register_member, name='register_member'),
    path('loan/', views.loan_information, name='loan'),
    path('edit-member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('teaching_staff/', views.teaching_staff, name='teaching_staff'),
    path('non_teaching_staff/', views.non_teaching_staff, name='non_teaching_staff'),
    path('details/<int:member_id>/', views.detail_members, name='detail_members'),
    path('next/', views.next_page, name='next_page'),
    path('loan_application/', views.loan_application, name='loan_application'),  
]
