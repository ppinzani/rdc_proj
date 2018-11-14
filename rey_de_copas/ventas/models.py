from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse

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
		null=True,
		blank=True,
	)

	promo = models.ForeignKey(
		'mercaderias.Promo',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
	)

	precio_unitario = models.DecimalField(
		max_digits=6,
		decimal_places=2,
	)


	class Meta:
		verbose_name = "DetalleDeVenta"
		verbose_name_plural = "DetallesDeVentas"

	def __str__(self):
		item = ""

		if self.promo:
			item = self.promo.get_detalle_full()
		elif self.mercaderia:
			item = self.mercaderia.descripcion

		return u"%s %s ($%s)" % (self.cantidad, item, self.get_subtotal())

	def get_descripcion(self):
		if self.promo:
			return self.promo.get_detalle_full()
		elif self.mercaderia:
			return self.mercaderia.descripcion

	def get_codigo(self):
		if self.promo:
			return self.promo.codigo
		elif self.mercaderia:
			return self.mercaderia.codigo

	def clean(self):
		if self.mercaderia is not None and self.promo is not None:
			raise ValidationError(
				_("Mercaderia y Promo debe no pueden tener valor a la vez")
			)


	def get_subtotal(self):
		return self.precio_unitario * self.cantidad



class Venta(models.Model):
	fecha_hora = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Venta"
		verbose_name_plural = "Ventas"


	def get_total(self):
		detalles = self.detalledeventa_set.all()
		return round(sum(d.get_subtotal() for d in detalles), 2)

	def get_absolute_url(self):
		return reverse('ventas:detalle', args=(self.id,))

	def get_delete_url(self):
		return reverse('ventas:borrar', args=(self.id,))

	def delete(self, *args, **kwargs):
		for detalle in self.detalledeventa_set.all():
			if detalle.mercaderia:
				detalle.mercaderia.stock.stock += detalle.cantidad
				detalle.mercaderia.stock.save()
			elif detalle.promo:
				for dp in detalle.promo.detallepromo_set.all():
					dp.mercaderia.stock.stock += (dp.cantidad * detalle.cantidad)
					dp.mercaderia.stock.save()
		return super(Venta, self).delete(*args, **kwargs)


