from django.urls import re_path

from . import views

app_name = 'mercaderias'

urlpatterns = [

    re_path(
        r'^$',
        views.MercaderiasList.as_view(),
        name='lista'
    ),

    re_path(
        r'^nueva$',
        views.CrearMercaderia.as_view(),
        name='nueva'
    ),

    re_path(r'^(?P<pk>[\w-]+)/editar$',
            view=views.ActualizarMercaderia.as_view(),
            name='editar'
            ),

    re_path(r'^(?P<pk>[\w-]+)/borrar$',
            view=views.EliminarMercaderia.as_view(),
            name='borrar'
            ),

    re_path(
        r'^promos/lista/$',
        view=views.PromosList.as_view(),
        name='lista_promos'
    ),

    re_path(
        r'^promos/nueva$',
        view=views.promo_cru,
        name='nueva_promo'
    ),

    re_path(
        r'^promos/(?P<pk>[\w-]+)/editar$',
        view=views.promo_cru,
        name='editar_promo'
    ),

    re_path(
        r'^promos/(?P<pk>[\w-]+)/borrar$',
        view=views.EliminarPromo.as_view(),
        name='borrar_promo'
    ),

    re_path(
        r'^promos/(?P<pk>[\w-]+)/$',
        view=views.PromoDetalle.as_view(),
        name='detalle_promo'
    ),

    re_path(
        r'^promos/imprimir-codigos$',
        view=views.ImprimirCodigos.as_view(),
        name='imprimir_codigos'
    ),
]
