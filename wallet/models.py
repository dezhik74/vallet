from django.db import models


class Transaction (models.Model):
    date_time = models.DateTimeField(auto_now_add=True);
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    comment = models.CharField(max_length=250)
    wallet = models.ForeignKey("Wallet", on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f'{self.comment} -> {str(self.value)}'

    def save(self, *args, **kwargs):
        print(self.value)
        super().save(*args, **kwargs)
        self.wallet.calc_balance()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.wallet.calc_balance()


class Wallet (models.Model):
    name = models.CharField(max_length=250)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)

    def calc_balance(self):
        print('calc balance')
        # TODO переделать на запрос в базу данных
        trs = self.transactions.all()
        if trs is not None:
            print(trs)
            new_balance = 0
            for tr in trs:
                new_balance += tr.value
            print(new_balance)
            self.balance = new_balance
            self.save()

    def __str__(self):
        return f'{self.name} -> {str(self.balance)}'
