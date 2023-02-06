from django.db import models


class Customer(models.Model):
    id: models.CharField = models.CharField(primary_key=True, max_length=32)
    first_name: models.CharField = models.CharField(max_length=32)
    last_name: models.CharField = models.CharField(max_length=32)
    address: models.CharField = models.CharField(max_length=256)
    phone: models.CharField = models.CharField(max_length=16)


class Account(models.Model):
    no: models.IntegerField = models.IntegerField(primary_key=True)
    name: models.CharField = models.CharField(max_length=32)
    type: models.CharField = models.CharField(max_length=32)
    owner: models.ForeignKey = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )
    balance: models.FloatField = models.FloatField(default=0.)
