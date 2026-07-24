from django.contrib import admin
from accounting_app.models import Transaction, TransactionCategory, Cheque


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind')
    list_filter = ('kind',)
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'amount', 'category', 'payment_method', 'occurred_at')
    list_filter = ('kind', 'payment_method', 'category')
    search_fields = ('title', 'description')
    date_hierarchy = 'occurred_at'


@admin.register(Cheque)
class ChequeAdmin(admin.ModelAdmin):
    list_display = ('cheque_number', 'direction', 'amount', 'counterparty', 'due_date', 'status')
    list_filter = ('direction', 'status', 'bank_name')
    search_fields = ('cheque_number', 'counterparty', 'description')
    date_hierarchy = 'due_date'
