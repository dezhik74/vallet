from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .models import Transaction, Wallet


class ModelTestCase (TestCase):

    def setUp(self) -> None:
        w1 = Wallet.objects.create(name='wallet 1')
        Transaction.objects.create(value=100.00, comment='trans 1', wallet=w1)
        Transaction.objects.create(value=200.00, comment='trans 2', wallet=w1)
        Transaction.objects.create(value=300.00, comment='trans 3', wallet=w1)
        w2 = Wallet.objects.create(name='wallet 2')
        Transaction.objects.create(value=10.00, comment='trans 2-1', wallet=w2)
        Transaction.objects.create(value=-10.00, comment='trans 2-2', wallet=w2)

    def test_wallet_balance(self):
        self.assertEqual(Wallet.objects.get(name='wallet 1').balance, 600.00)
        w1 = Wallet.objects.get(name='wallet 2')
        self.assertEqual(w1.balance, 0.00)
        t1 = Transaction.objects.get(comment='trans 2-2')
        t1.delete()
        w1 = Wallet.objects.get(name='wallet 2')
        # print(w2.name, w2.transactions.all())
        self.assertEqual(w1.balance, 10.00)
        Transaction.objects.create(value=-10.00, comment='trans 2-2', wallet=w1)
        self.assertEqual(w1.balance, 0.00)


class APITestCase (TestCase):

    def test_API(self):
        f = APIRequestFactory()
        response = f.get('wallets/')
        print(response)



