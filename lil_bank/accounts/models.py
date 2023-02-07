from django.db import models


class Customer(models.Model):
    id: models.CharField = models.CharField(primary_key=True, max_length=32)
    first_name: models.CharField = models.CharField(max_length=32)
    last_name: models.CharField = models.CharField(max_length=32)
    address: models.CharField = models.CharField(max_length=256)
    phone: models.CharField = models.CharField(max_length=16)


class Account(models.Model):
    no: models.AutoField = models.AutoField(primary_key=True)
    type: models.CharField = models.CharField(max_length=32, default="checking")
    owner: models.ForeignKey = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )
    balance: models.FloatField = models.FloatField(default=0.)


class Transaction(models.Model):
    account: models.ForeignKey = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
    )
    withdrawal: models.BooleanField = models.BooleanField()
    amount: models.FloatField = models.FloatField()
