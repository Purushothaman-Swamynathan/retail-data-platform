from django.db import models

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    amount = models.FloatField()
    fraud_flag = models.BooleanField()
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'transactions'

