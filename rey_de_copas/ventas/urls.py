from django.urls import re_path

from . import views

app_name = 'ventas'

urlpatterns = [

    re_path(
        r'lista_de_precios/$',
        views.ListaDePrecios.as_view(),
        name='lista_precios'
    ),

    re_path(
        r'cargar/$',
        views.cargar_venta,
        name='cargar'
    ),

    re_path(
        r'detalle_by_codigo/(?P<codigo>[\w-]+)/$',
        views.detalle_by_codigo,
        name='detalle_by_codigo'
    ),

]
