from django.db import models

# Create your models here.
class Pedido(models.Model):
    cantidad_ud = models.PositiveIntegerField()
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_articulo = models.CharField(max_length=255)
    codigo_articulo = models.CharField(max_length=46)
    nombre_proveedor = models.CharField(max_length=50)
    costo_envio_usd = models.DecimalField(max_digits=10, decimal_places=2)

#modelo de restados
class Resultados(models.Model):
    total_pedido_clp = models.DecimalField(max_digits=10, decimal_places=2)
    costo_envio_clp = models.DecimalField(max_digits=10, decimal_places=2,)
    impuesto_aduana_clp = models.DecimalField(max_digits=10, decimal_places=2)
    iva_clp = models.DecimalField(max_digits=10, decimal_places=2)
    total_impuestos_aduana_clp = models.DecimalField(max_digits=10, decimal_places=2)
    costo_total_compra_usd = models.DecimalField(max_digits=10, decimal_places=2)
    costo_total_compra_clp = models.DecimalField(max_digits=10, decimal_places=2)
    #se agrega la llaver secundaria
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)


