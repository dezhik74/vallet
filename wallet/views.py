from django.shortcuts import render
from rest_framework import generics
from .models import Wallet, Transaction
from .serializers import WalletListSerializer, TransactionSerializer, WalletDetailSerializer


class WalletList (generics.ListCreateAPIView):
    # список кошельков + создание кошелька
    queryset = Wallet.objects.all()
    serializer_class = WalletListSerializer


class WalletListDetail (generics.ListAPIView):
    # просто вывод списка кошельков с транзакциями
    queryset = Wallet.objects.all()
    serializer_class = WalletDetailSerializer


class WalletDetail (generics.RetrieveUpdateDestroyAPIView):
    # вывод одного кошелька с транзакциями, изменение имени кошелька, стирание кошелька
    queryset = Wallet.objects.all()
    serializer_class = WalletDetailSerializer


class TransactionDetail (generics.RetrieveUpdateDestroyAPIView):
    # вывод транзакции, стрирание транзакции, изменение транзакции
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionCreate (generics.CreateAPIView):
    # создание транзакции
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
