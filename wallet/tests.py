from django.test import TestCase
from .models import Transaction, Wallet
from rest_framework.test import APIClient
import json


class ModelTestCase (TestCase):

    def setUp(self) -> None:
        w1 = Wallet.objects.create(name='wallet 1')
        Transaction.objects.create(value=100.00, comment='trans 1', wallet=w1)
        Transaction.objects.create(value=200.00, comment='trans 2', wallet=w1)
        Transaction.objects.create(value=300.00, comment='trans 3', wallet=w1)
        w2 = Wallet.objects.create(name='wallet 2')
        Transaction.objects.create(value=10.00, comment='trans 2-1', wallet=w2)
        Transaction.objects.create(value=-10.00, comment='trans 2-2', wallet=w2)

    def test_str_functions(self):
        self.assertEqual(Wallet.objects.get(name='wallet 1').__str__(), 'wallet 1 -> 600.00')
        self.assertEqual(Transaction.objects.get(comment='trans 1').__str__(), 'trans 1 -> 100.00')

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
        # c = APIClient()
        # response = c.get('/wallets/')
        # print(response.status_code)
        # print(response.content_type)
        # print(response.content)

class APITestCase (TestCase):

    def setUp(self) -> None:
        m = ModelTestCase()
        m. setUp()
        self.c = APIClient()

    def test_wallets(self):
        # тест /wallets/ просто вывод всех кошельков с транзакциями
        response = self.c.get('/wallets/')
        # print(response.status_code)
        r = json.loads(response.content)
        # print(r[0])
        self.assertEqual(r[0]['transactions'][0]['value'], '100.00')

    def test_wallets_list(self):
        # тест /wallet-list/ вывод транзакций и изменение имени
        r = json.loads(self.c.get('/wallets-list/').content)
        # print(r[0])
        self.assertEqual(r[0]['name'], 'wallet 1')
        self.c.post('/wallets-list/', {'name': 'wallet 3'})
        r = json.loads(self.c.get('/wallets-list/').content)
        self.assertEqual(r[2]['name'], 'wallet 3')
        # print(r[2])
        r = self.c.get('/wallets-list/')
        self.assertContains(r, 'wallet 3')

    def test_wallet_detail(self):
        # тест /wallet/<pk> вывод транзакций, смена имени кошелька, удаление кошелька
        r = self.c.get('/wallet/1/')
        # print(r.content)
        self.assertContains(r, 'wallet 1')
        self.assertContains(r, 'trans 1')
        self.assertContains(r, 'trans 2')
        self.assertContains(r, 'trans 3')
        self.c.put('/wallet/1/', {'name': 'wallet 1 test'}, format='json')
        r = self.c.get('/wallets/')
        self.assertContains(r, 'wallet 1 test')
        self.c.delete('/wallet/1/')
        r = self.c.get('/wallets/')
        self.assertNotContains(r, 'wallet 1')

    def test_transaction_detail(self):
        # тест /transaction/<pk> выввод транзакции, удаление, смена суммы, наименования
        # чтение
        r = self.c.get('/transaction/1/')
        print(r.content)
        self.assertContains(r, '100.00')
        self.assertContains(r, 'trans 1')
        self.assertContains(r, '"wallet":1')
        # изменение
        self.c.patch('/transaction/1/', {'value': '14.00', 'comment': 'trans 1 test'}, format='json')
        r = self.c.get('/transaction/1/')
        # print(r.content)
        self.assertContains(r, '14.00')
        self.assertContains(r, 'trans 1 test')
        # удаление
        self.c.delete('/transaction/1/')
        r = self.c.get('/wallet/1/')
        self.assertNotContains(r, 'trans 1 test')









