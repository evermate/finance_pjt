# products/admin.py

from django.contrib import admin
from .models import Bank

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['kor_co_nm', 'fin_co_no']