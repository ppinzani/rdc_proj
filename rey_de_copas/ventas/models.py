from django.db import models

# Create your models here.
class DetalleDeVenta(models.Model):
	cantidad = models.PositiveSmallIntegerField()
	venta = models.ForeignKey(
		'ventas.Venta',
		on_delete=models.CASCADE,
	)
	mercaderia = models.ForeignKey(
		'mercaderias.Mercaderia',
		on_delete=models.SET_NULL,
		null=True
	)
	precio_unitario = models.DecimalField(
		max_digits=6,
		decimal_places=2,
	)

	class Meta:
		verbose_name = "DetalleDeVenta"
		verbose_name_plural = "DetallesDeVentas"

	def __str__(self):
		return u"%s %s ($%s)" % (self.cantidad,self.mercaderia.descripcion,self.get_subtotal())

	def get_subtotal(self):
		return self.precio_unitario * self.cantidad


class Venta(models.Model):
	fecha_hora = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Venta"
		verbose_name_plural = "Ventas"


	def get_total(self):
		detalles = DetalleDeVenta.objects.filter(venta=self)
		return round(sum(d.get_subtotal() for d in detalles), 2)


