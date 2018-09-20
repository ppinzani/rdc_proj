from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={
                               'class': 'form-control',
                               'placeholder': 'Ingresa tu nombre de usuario'}))
    password = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={
                               'type': 'password',
                               'class': 'form-control',
                               'placeholder': 'Ingresa tu password'}))
