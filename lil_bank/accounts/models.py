from django.db import models


class Customer(models.Model):
    id: models.CharField = models.CharField(primary_key=True, max_length=32)
    first_name: models.CharField = models.CharField(max_length=32)
    last_name: models.CharField = models.CharField(max_length=32)
    address: models.CharField = models.CharField(max_length=256)
    phone: models.CharField = models.CharField(max_length=16)

    def __repr__(self):
        return f'Customer[' \
                    f"id='{self.id}'," \
                    f"first_name='{self.first_name}'," \
                    f"last_name='{self.last_name}'," \
                    f"address='{self.address}'," \
                    f"phone='{self.phone}'" \
                ']'

    def __str__(self):
        return f'{self.id} : {self.first_name} {self.last_name}'


class Account(models.Model):
    no: models.AutoField = models.AutoField(primary_key=True)
    type: models.CharField = models.CharField(max_length=32, default="Checking")
    owner: models.ForeignKey = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )
    balance: models.FloatField = models.FloatField(default=0.)

    def __repr__(self):
        return f'Account[' \
                    f'no={self.no},' \
                    f"type='{self.type}'," \
                    f'owner={self.owner},' \
                    f'balance={self.balance}' \
                ']'

    def __str__(self):
        return f'{self.no} : {self.type}'


class Transaction(models.Model):
    account: models.ForeignKey = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
    )
    withdrawal: models.BooleanField = models.BooleanField()
    amount: models.FloatField = models.FloatField()

    def __repr__(self):
        return f'Account[' \
                    f'account={self.account},' \
                    f'withdrawal={self.withdrawal},' \
                    f'amount={self.amount}' \
                ']'

    def __str__(self):
        return f'{self.id} : ' \
               f"{'Deposit' if not self.withdrawal else 'Withdrawal'} " \
               f'({self.amount})'
