from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    '''
        Admin View for Order
    '''
    list_display = ('email', 'transaction_id', 'timestamp')
    search_fields = ('email', 'transaction_id')

admin.site.register(Order, OrderAdmin)
