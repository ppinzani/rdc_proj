from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

import json

from .forms import CargaStockForm
from mercaderias.models import Mercaderia
from .models import Stock


# Create your views here.
class StockList(LoginRequiredMixin, ListView):
    model = Stock
    queryset = Stock.objects.all().order_by('mercaderia')
    template_name = 'stock/stock_lista.html'
    context_object_name = 'stock_items'
    redirect_field_name = '/login/'


"""
	View para la pag de cargar stock
"""
@login_required
def cargar_stock(request):
	if request.method == 'POST':
		if request.is_ajax():
			codigos = request.POST.getlist("codigos[]")
			cantidades = request.POST.getlist("cantidades[]")
			editar = "editar" in request.POST

			for cod,cant in zip(codigos, cantidades):
				mercaderia = Mercaderia.objects.get(codigo=cod)
				if not editar:
					mercaderia.stock.stock += int(cant)
				else:
					mercaderia.stock.stock = int(cant)
				mercaderia.stock.save()

			return HttpResponse(status=200) # OK

	else:
		carga_form = CargaStockForm()

	mercaderias_options = {m.descripcion: m.codigo for m in Mercaderia.objects.all()}
	mercaderias_options = json.dumps(mercaderias_options)

	variables = {
		'form': carga_form,
		'options_dict': mercaderias_options
	}

	template = 'stock/cargar_stock.html'

	return render(request, template, variables)


@login_required
def mercaderia_by_codigo(request, codigo):
	if request.method == 'GET':
		ret_str = """<tr>
						<td class="stock_item_cod">CODIGO</td>
						<td class="stock_item_desc">DESCRIPCION</td>
						<td class="stock_item_cant">CANTIDAD</td>
						<td class="text-right">
							<div class="btn btn-warning btn-editar"><span class="glyphicon glyphicon-pencil"></span></div>
							<div class="btn btn-danger btn-eliminar"><span class="glyphicon glyphicon-trash"></span></div>
						</td>
					</tr> """

		try:
			mercaderia_item = Mercaderia.objects.get(codigo=codigo)
		except:
			return HttpResponse("")

		ret_str = ret_str.replace("CODIGO", mercaderia_item.codigo)\
			.replace("DESCRIPCION", mercaderia_item.descripcion)\
			.replace("CANTIDAD", str(mercaderia_item.unidades_por_caja))


		return HttpResponse(ret_str)
	else:
		return HttpResponse(status=405) # Method not allowed

