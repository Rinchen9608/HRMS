from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=1)
    date_of_birth = models.DateField()
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    appointment_date = models.DateField()

    USERNAME_FIELD = "name" 
