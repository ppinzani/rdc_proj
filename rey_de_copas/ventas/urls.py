from django.urls import re_path

from . import views

app_name = 'ventas'

urlpatterns = [

    re_path(
        r'^$',
        views.ListaVentas.as_view(),
        name='lista'
    ),

    re_path(
        r'^lista_de_precios/$',
        views.ListaDePrecios.as_view(),
        name='lista_precios'
    ),

    re_path(
        r'^cargar$',
        views.venta_cru,
        name='cargar'
    ),

    re_path(
        r'^detalle_by_codigo/(?P<codigo>[\w-]+)/$',
        views.detalle_by_codigo,
        name='detalle_by_codigo'
    ),

    re_path(
        r'^(?P<pk>[\d]+)$',
        view=views.VentaDetalle.as_view(),
        name='detalle'
    ),

]
