from django.db import models

from annoying.fields import AutoOneToOneField

#Create your models here.
class Stock(models.Model):
	mercaderia = AutoOneToOneField(
		'mercaderias.Mercaderia',
		on_delete = models.CASCADE
	)

	stock = models.PositiveIntegerField(
		default=0
	)

	class Meta:
		verbose_name = "Stock"

	def __str__(self):
		return u"%s" % self.stock
