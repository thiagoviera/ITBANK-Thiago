from django.db import models

# Create your models here.

class Tarjeta(models.Model):
    card_id = models.IntegerField()
    card_numero = models.IntegerField() 
    card_expiracion_fecha = models.TextField()
    card_emision_fecha = models.TextField()
    card_cvv = models.CharField(max_length=200)
    card_tipo = models.TextField()
    customer_id = models.IntegerField()
    card_brand_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tarjeta'
