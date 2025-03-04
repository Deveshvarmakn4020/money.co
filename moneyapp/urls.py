from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('home/', views.home, name='home'),
    path('reg-member/', views.register_member, name='register_member'),
    path('loan/', views.loan_information, name='loan'),
    path('members/', views.members_list, name='members'),
    path('edit-member/<int:member_id>/', views.edit_member, name='edit_member'),  # Edit URL
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),  # Delete URL
    path('teaching_staff/', views.teaching_staff, name='teaching_staff'),
    path('non_teaching_staff/', views.non_teaching_staff, name='non_teaching_staff'),
    path('details/<int:member_id>/', views.detail_members, name='detail_members'),
    path('edit-member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
]
