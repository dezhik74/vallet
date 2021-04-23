from django.db import models
from django.db.models import Sum, DecimalField, Q


class Transaction (models.Model):
    date_time = models.DateTimeField(auto_now_add=True);
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)
    comment = models.CharField(max_length=250)
    wallet = models.ForeignKey("Wallet", on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f'{self.comment} -> {str(self.value)}'

    def save(self, *args, **kwargs):
        # print(self.value)
        super().save(*args, **kwargs)
        self.wallet.calc_balance()

    def delete(self, *args, **kwargs):
        r = super().delete(*args, **kwargs)
        # print('delete ', self)
        self.wallet.calc_balance()
        return r


class Wallet (models.Model):
    name = models.CharField(max_length=250)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True)

    def calc_balance(self):
        res = Transaction.objects.aggregate(sum=Sum('value', output_field=DecimalField(), filter=Q(wallet__pk=self.pk)))
        if res:
            self.balance = res['sum']
            self.save()

    def __str__(self):
        return f'{self.name} -> {str(self.balance)}'
