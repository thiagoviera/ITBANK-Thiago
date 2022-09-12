from django.db import models

# Create your models here.



class Empleado(models.Model):
    employee_id = models.IntegerField()
    employee_name = models.TextField()
    employee_surname = models.TextField()
    employee_hire_date = models.TextField()
    employee_dni = models.TextField(db_column='employee_DNI')  # Field name made lowercase.
    branch_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'empleado'

class Movimientos(models.Model):
    movimiento_id = models.IntegerField()
    customer_id = models.TextField()

    class Meta:
        managed = False
        db_table = 'movimientos'
