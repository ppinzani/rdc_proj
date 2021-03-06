import json

from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.core.exceptions import EmptyResultSet
from django.forms import formset_factory
from django.contrib import messages

from mercaderias.models import Mercaderia, Promo
from .models import DetalleDeVenta, Venta
from .forms import DetalleVentaForm
from mercaderias.helpers import MercaderiaPromoAdapter


# Create your views here.
class ListaVentas(LoginRequiredMixin, ListView):
    model = Venta
    template_name = 'ventas/lista_ventas.html'
    context_object_name = 'ventas'
    queryset = Venta.objects.all().order_by("-fecha_hora")
    redirect_field_name = '/'


class ListaDePrecios(LoginRequiredMixin, ListView):
    model = Mercaderia
    queryset = Mercaderia.objects.filter(activa=True)
    template_name = 'ventas/lista_precios.html'
    context_object_name = 'mercaderias'
    redirect_field_name = '/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['promos'] = Promo.objects.all()
        return data


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
                mpa = MercaderiaPromoAdapter(cod)
                mpa.process_stock(int(cant))
                if isinstance(mpa.item, Mercaderia):
                    detalles.append(
                        DetalleDeVenta(
                            cantidad=int(cant),
                            venta=venta,
                            mercaderia=mpa.item,
                            precio_unitario=float(precio),
                        )
                    )
                else:
                    detalles.append(
                        DetalleDeVenta(
                            cantidad=int(cant),
                            venta=venta,
                            promo=mpa.item,
                            precio_unitario=float(precio)
                        )
                    )
            try:
                with transaction.atomic():
                    DetalleDeVenta.objects.bulk_create(detalles)
                    return redirect(reverse("ventas:lista"))
            except IntegrityError:
                DetalleDeVenta.objects.filter(venta=venta).delete()
                venta.delete()
                return HttpResponse(status=200)  # FIXME

    template = 'ventas/cargar_venta.html'

    return render(request, template)


@login_required
def venta_cru(request):
    DetalleFormset = formset_factory(DetalleVentaForm)

    if request.method == "GET":
        formset = DetalleFormset()

    elif request.method == "POST":
        formset = DetalleFormset(request.POST)
        has_error = False

        if formset.is_valid():
            venta = Venta.objects.create()

            detalles = []
            for i, form in enumerate(formset):
                if i != 0 and form.is_valid():
                    codigo = form.cleaned_data.get('codigo')
                    cantidad = form.cleaned_data.get('cantidad')
                    precio_unit = form.cleaned_data.get('precio_unitario')

                    mpa = MercaderiaPromoAdapter(codigo)

                    try:
                        mpa.process_stock(cantidad)
                    except IntegrityError as e:
                        venta.delete()
                        messages.error(
                            request,
                            e.args[0]
                        )
                        has_error = True

                    if isinstance(mpa.item, Mercaderia):
                        ganancia = cantidad*(precio_unit - mpa.item.precio_compra)
                        detalles.append(
                            DetalleDeVenta(
                                cantidad=cantidad,
                                venta=venta,
                                mercaderia=mpa.item,
                                precio_unitario=precio_unit,
                                ganancia=ganancia
                            )
                        )
                    else:
                        ganancia = cantidad*(precio_unit - mpa.item.get_precio_compra())
                        detalles.append(
                            DetalleDeVenta(
                                cantidad=cantidad,
                                venta=venta,
                                promo=mpa.item,
                                precio_unitario=precio_unit,
                                ganancia=ganancia
                            )
                        )
            if not has_error:
                with transaction.atomic():
                    try:
                        DetalleDeVenta.objects.bulk_create(detalles)
                        return redirect(reverse("ventas:lista"))
                    except IntegrityError:
                        DetalleDeVenta.objects.filter(venta=venta).delete()
                        venta.delete()
                        messages.error(
                            request,
                            "Error Grabando la promo, Intente de Nuevo"
                        )

    mercaderias_options = {m.descripcion: m.codigo for m in Mercaderia.objects.all()}
    promos_options = {p.get_detalle_full(): p.codigo for p in Promo.objects.all()}
    mercaderias_options.update(promos_options)
    mercaderias_options = json.dumps(mercaderias_options)

    template = 'ventas/cargar_venta.html'

    variables = {
        "formset": formset,
        "options_dict": mercaderias_options,
    }

    return render(request, template, variables)


@login_required
def mercaderia_by_codigo(request, codigo):
    if request.method == 'GET':

        try:
            mpa = MercaderiaPromoAdapter(codigo)
        except EmptyResultSet:
            return HttpResponse("")

        ret = {
            'codigo': str(mpa.codigo),
            'descripcion': str(mpa.descripcion),
            'cantidad': "1",
            'precio_unitario': str(mpa.precio_venta),
        }

        ret = json.dumps(ret)

        return HttpResponse(ret)
    else:
        return HttpResponse(status=405)  # Method not


class VentaDetalle(LoginRequiredMixin, DetailView):
    model = Venta
    template_name = 'ventas/detalle_venta.html'
    context_object_name = 'venta'
    redirect_field_name = '/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['detalles'] = data['venta'].detalledeventa_set.all()
        return data


class BorrarVenta(LoginRequiredMixin, DeleteView):
    model = Venta
    template_name = 'ventas/eliminar_venta.html'
    success_url = '/ventas/'
    redirect_field_name = '/'