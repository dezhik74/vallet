from django.urls import path
from .views import WalletList, WalletListDetail, WalletDetail, TransactionDetail, TransactionCreate

urlpatterns = [
    path('wallets/', WalletListDetail.as_view(), name='wallet_list_detail_url'),
    path('wallets-list/', WalletList.as_view(), name='wallet_list_url'),
    path('wallet/<int:pk>/', WalletDetail.as_view(), name='wallet_detail_url'),
    path('transaction/<int:pk>/', TransactionDetail.as_view(), name='transaction_detail_url'),
    path('transaction-new/', TransactionCreate.as_view(), name='transaction_detail_url'),

]