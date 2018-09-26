from django import forms

from .models import DetalleDeVenta


class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleDeVenta
        fields = ['cantidad', 'precio_unitario']
        widgets = {
            'cantidad': forms.NumberInput(
                attrs={'class': 'form-control cantidad  '}
            ),
            'precio_unitario': forms.NumberInput(
                attrs={'class': 'form-control precio-unitario'}
            )
        }

    detalle = forms.CharField(max_length=200,
                              widget=forms.TextInput(
                                  attrs={
                                      'class': "form-control",
                                      'readonly': True,
                                  }
                              ))

    codigo = forms.CharField(max_length=50,
                             widget=forms.TextInput(
                                 attrs={
                                     'class': "form-control",
                                     'readonly': True,
                                 }
                             ))
