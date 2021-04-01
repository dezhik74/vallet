from django.contrib import admin
from .models import Wallet, Transaction

class TransactionInLine (admin.StackedInline):
    model = Transaction
    extra = 1


@admin.register (Wallet)
class WalletAdmin (admin.ModelAdmin):
    list_display = ('name', 'balance')
    inlines = [TransactionInLine]

@admin.register(Transaction)
class TransactionAdmin (admin.ModelAdmin):
    pass
