from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('reg-member/', views.register_member, name='register_member'),
    path('loan/', views.loan_information, name='loan'),
    path('edit-member/<int:member_id>/', views.edit_member, name='edit_member'),  # Edit URL
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),  # Delete URL
    path('teaching_staff/', views.teaching_staff, name='teaching_staff'),
    path('non_teaching_staff/', views.non_teaching_staff, name='non_teaching_staff'),

]
