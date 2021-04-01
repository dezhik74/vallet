from rest_framework import serializers

from .models import Transaction, Wallet


class TransactionSerializer (serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class WalletListSerializer (serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'name', 'balance')
        read_only_fields = ('balance',)


class WalletDetailSerializer (serializers.ModelSerializer):

    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ('id', 'name', 'balance', 'transactions')
        read_only_fields = ('balance',)