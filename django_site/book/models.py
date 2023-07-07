import datetime
from django.db import models

# Create your models here.
class Book(models.Model):
    titulo=models.CharField(max_length=100)
    autor=models.CharField(max_length=100)
    valoracion=models.IntegerField(help_text='Valoracion entre 0 y 100')
    fecha_creacion =models.DateField(default= datetime.datetime.now)
    fecha_modificacion =models.DateField(default= datetime.datetime.now)



    class Meta:
        verbose_name ='Libro'
        verbose_name_plural = 'Libros'
        permissions = [
            ('development','permiso como desarrollador'),
            ('scrum_master','permiso como scrum_master'),
            ('product_owner', 'permiso como product_owner')
        ]