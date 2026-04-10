from django.contrib import admin
from .models import Item, Transaction, Alert, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'unit', 'status', 'last_updated')
    list_filter = ('category', 'status')
    search_fields = ('name', 'supplier')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('item', 'type', 'quantity', 'date', 'user')
    list_filter = ('type', 'date')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('severity', 'item_name', 'type', 'date')
    list_filter = ('severity', 'type')
