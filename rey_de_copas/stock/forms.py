from django import forms

from mercaderias.models import Mercaderia


class CargaStockForm(forms.Form):
	codigo = forms.CharField(label="Código de Barra",
							 max_length=50,
							 widget=forms.Textarea(
								 attrs={
									 'class': "form-control"
								 }
							 ))