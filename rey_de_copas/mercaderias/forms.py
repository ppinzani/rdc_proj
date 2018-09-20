from django import forms
from dal import autocomplete

from .models import Mercaderia
from .models import Promo, DetallePromo


class MercaderiaForm(forms.ModelForm):
    class Meta:
        model = Mercaderia
        fields = ['codigo', 'descripcion', 'precio_compra', 'precio_venta',
                  'unidades_por_caja']
        widgets = {
            'codigo': forms.TextInput(
                attrs={
                    'placeholder': 'Código de Barra',
                    'class': 'form-control'
                }
            ),
            'descripcion': forms.TextInput(
                attrs={
                    'placeholder': 'Descripción',
                    'class': 'form-control'
                }
            ),
            'precio_compra': forms.NumberInput(
                attrs={
                    'label-tag': 'Precio de Compra',
                    'class': 'form-control'
                }
            ),
            'precio_venta': forms.NumberInput(
                attrs={
                    'label-tag': 'Precio de Venta',
                    'class': 'form-control'
                }
            ),
            'unidades_por_caja': forms.NumberInput(
                attrs={
                    'label-tag': 'Unidades por Caja',
                    'class': 'form-control'
                }
            ),
        }


class DetallePromoForm(forms.ModelForm):
    class Meta:
        model = DetallePromo
        fields = ['cantidad']
        widgets = {
            'cantidad': forms.NumberInput(
                attrs={'placeholder': 'Cantidad', 'class': 'form-control'}
            )
        }

    mercaderia = forms.CharField(label="Descripcion",
                             max_length=200,
                             widget=forms.TextInput(
                                 attrs={
                                     'class': "form-control",
                                     'readonly': True,
                                 }
                             ))


class PromoForm(forms.ModelForm):
    class Meta:
        model = Promo
        fields = ['nombre', 'precio']
        widgets = {
            'precio': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control'}
            )
        }
