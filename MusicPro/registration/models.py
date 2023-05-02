from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True, default=2)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    contrasena = models.CharField(max_length=128)
    tipo_cuenta = models.CharField(max_length=10)
    
    def __str__(self):
        return self.nombre