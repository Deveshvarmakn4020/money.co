# moneyapp/admin.py
from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'member_id', 'department', 'mob']
    search_fields = ['name', 'member_id']
from django.contrib import admin

# Register your models here.
