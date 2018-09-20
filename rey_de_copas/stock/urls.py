from django.urls import re_path

from . import views

app_name = 'stock'

urlpatterns = [

	re_path(
		r'^$',
		views.StockList.as_view(),
		name='lista'
	),

	re_path(
		r'cargar/$',
		views.cargar_stock,
		name='cargar'
	),

	re_path(
		r'mercaderia_by_codigo/(?P<codigo>[\w-]+)/$',
		views.mercaderia_by_codigo,
		name='mercaderia_by_codigo'
	),
]