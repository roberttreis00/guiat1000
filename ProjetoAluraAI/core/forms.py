from django import forms

class Cidade(forms.Form):
    city = forms.CharField(max_length=50, label='cidade')