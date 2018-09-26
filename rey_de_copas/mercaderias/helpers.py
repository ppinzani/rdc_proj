from .models import Promo, Mercaderia
from django.core.exceptions import EmptyResultSet


class MercaderiaPromoAdapter:

	def __init__(self, codigo):

		self.codigo = codigo
		mercaderia = Mercaderia.objects.filter(codigo=codigo)
		promo = Promo.objects.filter(codigo=codigo)


		if mercaderia:
			mercaderia = mercaderia.first()
			self.item = mercaderia
			self.precio_venta = mercaderia.precio_venta
			self.precio_compra = mercaderia.precio_compra
			self.unidades_por_caja = mercaderia.unidades_por_caja
			self.descripcion = mercaderia.descripcion
		elif promo:
			promo = promo.first()
			self.item = promo
			self.precio_venta = promo.precio
			self.precio_compra = 0
			self.unidades_por_caja = 0
			self.descripcion = promo.get_detalle_full()
		else:
			raise EmptyResultSet()


	def process_stock(self, cantidad):
		if isinstance(self.item, Mercaderia):
			self.item.stock.stock = self.item.stock.stock - cantidad
			self.item.stock.save()
		elif isinstance(self.item, Promo):
			# Proceso stock de la promo
			for detalle in self.item.detallepromo_set.all():
				detalle.mercaderia.stock.stock -= (cantidad * detalle.cantidad)
				detalle.mercaderia.stock.save()


