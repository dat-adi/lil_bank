from django.contrib import admin
from .models import Customer, Account, Transaction


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Account)
admin.site.register(Transaction)