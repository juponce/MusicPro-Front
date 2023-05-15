from django.db import models

# Create your models here.
class Carrito(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)

    def get_total_cart(self, i):
        itemscarrito = self.itemcarrito_set.all()
        total = round(sum([item.get_total for item in itemscarrito]) * i)
        return total


    def get_sub_total(self):
        itemscarrito = self.itemcarrito_set.all()
        sub_total = sum([item.get_total for item in itemscarrito])
        return sub_total

class ItemCarrito(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.IntegerField(null=True, blank=True)
    producto = models.CharField(max_length=200)
    carrito = models.ForeignKey(Carrito, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    precio = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.producto.precio * self.cantidad
        return total
    
    @property
    def get_stock(self):
        number_list = list(range(1, self.producto.stock+1))
        return number_list
