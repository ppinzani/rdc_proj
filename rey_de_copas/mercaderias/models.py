from random import randint
from datetime import datetime
from barcode import generate

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File

from stock.models import Stock


# Create your models here.
class Mercaderia(models.Model):
    codigo = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(unique=True, max_length=100)
    precio_compra = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True
    )
    precio_venta = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        blank=True,
        null=True
    )
    unidades_por_caja = models.PositiveSmallIntegerField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Mercaderia"
        verbose_name_plural = "Mercaderias"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not Stock.objects.filter(mercaderia=self).exists():
            stock = Stock(mercaderia=self, stock=0)
            stock.save()

    def __str__(self):
        return u"%s" % self.descripcion

    def get_update_url(self):
        return reverse('mercaderias:editar', args=(self.id,))

    def get_delete_url(self):
        return reverse('mercaderias:borrar', args=(self.id,))


"""
Auxiliar function to generate barcode
"""


def get_barcode():
    code = str(randint(1, 999999999)).zfill(9)  # 9 random digits
    code = "950" + code
    #Checksum Process
    digits = [*map(int, reversed(code))]
    even, odd = digits[0::2], digits[1::2]
    number = sum(odd) + sum(even) * 3
    number = (10 - number) % 10
    return code + str(number)


class Promo(models.Model):
    codigo = models.CharField(
        max_length=100,
        default=get_barcode,
        unique=True
    )
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    nombre = models.CharField(max_length=100, blank=True)
    imagen_codigo = models.FileField(upload_to="barcodes/", null=True)


    class Meta:
        verbose_name = 'Promo'
        verbose_name_plural = 'Promos'

    def __str__(self):
        if self.nombre != "":
            return u"%s" % self.nombre
        else:
            return self.get_detalle()

    def get_update_url(self):
        return reverse('mercaderias:editar_promo', args=(self.id,))

    def get_delete_url(self):
        return reverse('mercaderias:borrar_promo', args=(self.id,))

    def get_absolute_url(self):
        return reverse('mercaderias:detalle_promo', args=(self.id,))

    def get_detalle(self):
        detalles = self.detallepromo_set.all()
        s = " + ".join(map(str, detalles))
        return u"%s" % s

    def get_detalle_full(self):
        return f"{self.nombre}({self.get_detalle()})"

    def get_precio_compra(self):
        return sum((det.get_precio_compra() for det in self.detallepromo_set.all()))

    def get_barcode_image_url(self):
        return f"{settings.MEDIA_URL}barcodes/{self.codigo}.svg"

    def get_barcode_location(self):
        return self.get_barcode_image_url().replace(settings.MEDIA_URL, settings.MEDIA_ROOT + "/")

    def get_image_tmp_location(self):
        return f"/tmp/{self.codigo}.svg"

    def create_barcode_image(self):
        output_filename = self.get_image_tmp_location()[:-4]
        generate("EAN13", self.codigo, output=output_filename)

    #def save(self, *args, **kwargs):
        #super().save(*args, **kwargs)
        #self.create_barcode_image()
        #with open(self.get_image_tmp_location()) as file:
        #    df = File(file)
        #    self.imagen_codigo.save("new", df)

        #image_filepath = self.get_barcode_location()
        #if not default_storage.exists(image_filepath):
        #    self.create_barcode_image()

    #def delete(self, *args, **kwargs):
    #    image_location = self.get_barcode_location()
    #    if default_storage.exists(image_location):
    #        default_storage.delete(image_location)
    #    return super(Promo, self).delete(*args, **kwargs)


class DetallePromo(models.Model):
    cantidad = models.PositiveSmallIntegerField(blank=True)
    mercaderia = models.ForeignKey(
        'mercaderias.Mercaderia',
        on_delete=models.SET_NULL,
        null=True
    )
    promo = models.ForeignKey(
        'mercaderias.Promo',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Detalle De Promo'
        verbose_name_plural = "Detalles de Promo"

    def __str__(self):
        return u"{} {}".format(self.cantidad, str(self.mercaderia))

    def get_precio_compra(self):
        return self.mercaderia.precio_compra * self.cantidad
