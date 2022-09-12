from django.db import models

# Create your models here.

class Cuenta(models.Model):
    account_id = models.IntegerField()
    customer_id = models.IntegerField()
    balance = models.IntegerField()
    iban = models.TextField()

    class Meta:
        managed = False
        db_table = 'cuenta'
