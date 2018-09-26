from django import forms
from django.forms import BaseFormSet

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
                             required=False,
                             widget=forms.TextInput(
                                 attrs={
                                     'class': "form-control",
                                     'readonly': True,
                                 }
                             ))

    def fields_required(self, fields):
        """Used for conditionally marking fields as required."""
        for field in fields:
            if not self.cleaned_data.get(field, ''):
                msg = forms.ValidationError("Este campo no puede ser nulo.")
                self.add_error(field, msg)

    def clean(self):
        mercaderia = self.cleaned_data.get('mercaderia')

        if mercaderia:
            self.fields_required(['cantidad'])

        return self.cleaned_data


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