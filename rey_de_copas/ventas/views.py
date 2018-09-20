from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction

from mercaderias.models import Mercaderia
from .models import DetalleDeVenta, Venta

# Create your views here.
class ListaDePrecios(LoginRequiredMixin, ListView):
    model = Mercaderia
    queryset = Mercaderia.objects.filter(activa=True)
    template_name = 'ventas/lista_precios.html'
    context_object_name = 'mercaderias'
    redirect_field_name = '/'


def cargar_venta(request):
    if request.method == "GET":
        pass
    else:
        if request.is_ajax():
            #Creo la venta y agrego los detalles
            venta = Venta.objects.create()
            detalles = []
            detalles_string = request.POST.getlist('strings[]')


            for s in detalles_string:
                cod, cant, precio = s.split(" ")
                mercaderia = Mercaderia.objects.get(codigo=int(cod))
                mercaderia.stock.stock = mercaderia.stock.stock - int(cant)
                mercaderia.stock.save()
                detalles.append(
                    DetalleDeVenta(
                        cantidad=int(cant),
                        venta=venta,
                        mercaderia=mercaderia,
                        precio_unitario=float(precio)
                    )
                )

            try:
                with transaction.atomic():
                    DetalleDeVenta.objects.bulk_create(detalles)
                    return HttpResponse(status=200)  # FIXME
            except IntegrityError:
                DetalleDeVenta.objects.filter(venta=venta).delete()
                venta.delete()
                return HttpResponse(status=200)  # FIXME




    variables = {}

    template = 'ventas/cargar_venta.html'

    return render(request, template, variables)


@login_required
def detalle_by_codigo(request, codigo):
    if request.method == 'GET':
        ret_str = \
        """
            <tr>
            <td class="detalle_cod">CODIGO</td>
            <td class="detalle_cant">CANTIDAD</td>
            <td class="detalle_desc">DESCRIPCION</td>
            <td class="detalle_pu">PRECIO_UN</td>
            <td class="detalle_subt">SUBTOTAL</td>
            <td>
                <div class="btn btn-warning btn-editar"><span class="glyphicon glyphicon-pencil"></span></div>
                <div class="btn btn-danger btn-eliminar"><span class="glyphicon glyphicon-trash"></span></div>
            </td>
            </tr>
        """

        try:
            mercaderia_item = Mercaderia.objects.get(codigo=codigo)
        except:
            return HttpResponse("")

        ret_str = ret_str.replace("CODIGO", mercaderia_item.codigo)\
            .replace("DESCRIPCION", mercaderia_item.descripcion)\
            .replace("CANTIDAD", "1")\
            .replace("PRECIO_UN", str(mercaderia_item.precio_venta))\
            .replace("SUBTOTAL", str(mercaderia_item.precio_venta))

        return HttpResponse(ret_str)
    else:
        return HttpResponse(status=405) # Method not allowed