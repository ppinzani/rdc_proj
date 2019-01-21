from .models import Promo, Mercaderia
from django.core.exceptions import EmptyResultSet
from django.db import IntegrityError


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
			try:
				self.item.stock.stock = self.item.stock.stock - cantidad
				self.item.stock.save()
			except IntegrityError:
				raise IntegrityError(f"Error: stock de {self.item.descripcion} no puede ser negativo")
		elif isinstance(self.item, Promo):
				# Proceso stock de la promo
				for detalle in self.item.detallepromo_set.all():
					try:
						detalle.mercaderia.stock.stock -= (cantidad * detalle.cantidad)
						detalle.mercaderia.stock.save()
					except IntegrityError:
						raise IntegrityError(f"Error: stock de {detalle.mercaderia.descripcion} no puede ser negativo")


