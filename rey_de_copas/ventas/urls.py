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
        r'^mercaderia_by_codigo/(?P<codigo>[\d]+)/$',
        views.mercaderia_by_codigo,
        name='mercaderia_by_codigo'
    ),

    re_path(
        r'^(?P<pk>[\d]+)/borrar$',
        view=views.BorrarVenta.as_view(),
        name='borrar'
    ),

    re_path(
        r'^(?P<pk>[\d]+)$',
        view=views.VentaDetalle.as_view(),
        name='detalle'
    ),
]
