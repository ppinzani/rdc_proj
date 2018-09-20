import json

from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, reverse
from django.db import IntegrityError, transaction

from .models import Mercaderia
from .models import DetallePromo, Promo
from .forms import MercaderiaForm
from .forms import PromoForm, DetallePromoForm


# Create your views here.
class MercaderiasList(LoginRequiredMixin, ListView):
    model = Mercaderia
    queryset = Mercaderia.objects.filter(activa=True)
    template_name = 'mercaderias/mercaderias_lista.html'
    # This setting gives the queried data a helpful name.
    # This name can then be later used in templates.
    context_object_name = 'mercaderias'
    redirect_field_name = '/'


class CrearMercaderia(LoginRequiredMixin, CreateView):
    form_class = MercaderiaForm
    template_name = 'mercaderias/create_update_mercaderias.html'
    model = Mercaderia
    success_url = '/mercaderias/'
    redirect_field_name = '/'


class ActualizarMercaderia(LoginRequiredMixin, UpdateView):
    form_class = MercaderiaForm
    template_name = 'mercaderias/create_update_mercaderias.html'
    model = Mercaderia
    success_url = '/mercaderias/'
    redirect_field_name = '/'


class EliminarMercaderia(LoginRequiredMixin, DeleteView):
    model = Mercaderia
    success_url = '/mercaderias/'
    template_name = 'mercaderias/eliminar_mercaderia.html'
    redirect_field_name = '/'


@login_required
def promo_cru(request):
    DetalleFormset = formset_factory(DetallePromoForm)

    if request.method == 'GET':
        mercaderias_options = [m.descripcion for m in Mercaderia.objects.all()]
        mercaderias_options = json.dumps(mercaderias_options)

        formset = DetalleFormset()

        promo_form = PromoForm()

        variables = {
            'options': mercaderias_options,
            'formset': formset,
            'promo_form': promo_form,
        }

        template = "mercaderias/create_update_promo.html"

        return render(request, template, variables)
    else:
        promo_form = PromoForm(request.POST)
        formset = DetalleFormset(request.POST)

        if promo_form.is_valid() and formset.is_valid():
            promo = promo_form.save()

            detalles = []
            for i, form in enumerate(formset):
                if i != 0:
                    cantidad = form.cleaned_data.get('cantidad')
                    desc = form.cleaned_data.get('mercaderia')

                    mercaderia = get_object_or_404(Mercaderia, descripcion=desc)

                    if cantidad and mercaderia:
                        detalles.append(
                            DetallePromo(
                                cantidad=cantidad,
                                mercaderia=mercaderia,
                                promo=promo,
                            )
                        )
            with transaction.atomic():
                try:
                    DetallePromo.objects.bulk_create(detalles)
                except:
                    pass

            return redirect(reverse("mercaderias:lista_promos"))


class PromosList(LoginRequiredMixin, ListView):
    model = Promo
    template_name = 'mercaderias/promos_lista.html'
    # This setting gives the queried data a helpful name.
    # This name can then be later used in templates.
    context_object_name = 'promos'
    redirect_field_name = '/'


class DetallePromo(LoginRequiredMixin, DetailView):
    model = Promo
    template_name = 'mercaderias/detalle_promo.html'
    context_object_name = 'promo'
    redirect_field_name = '/'


class EliminarPromo(LoginRequiredMixin, DeleteView):
    model = Promo
    success_url = '/mercaderias/promos'
    template_name = 'mercaderias/eliminar_promo.html'
    redirect_field_name = '/'
