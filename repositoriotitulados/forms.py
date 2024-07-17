from seg_mod_graduacion.models import ActividadRepositorio, PERIODO_CHOICES,Modalidad
from django import forms

import datetime

current_year = datetime.datetime.now().year
YEAR_CHOICES = [(year, year) for year in range(1990, current_year + 1)]

class TransferirActividadForm(forms.Form):
    periodo = forms.ChoiceField(choices=PERIODO_CHOICES) 
    anio_ingreso = forms.ChoiceField(
        label='Año de Ingreso',
        choices=YEAR_CHOICES,
        initial=current_year,  # Establece el año actual como valor inicial
        widget=forms.Select(attrs={'id': 'anio_ingreso', 'size': 2})  # Ajusta el tamaño del selector
    )
    anio_egreso = forms.ChoiceField(
        label='Año de Egreso',
        choices=YEAR_CHOICES,
        initial=current_year,  # Establece el año actual como valor inicial
        widget=forms.Select(attrs={'id': 'anio_egreso', 'size': 2})  # Ajusta el tamaño del selector
    )
    numero_acta = forms.CharField(label='Número de Acta', max_length=50)
    nota_aprobacion = forms.DecimalField(label='Nota de Aprobación', max_digits=4, decimal_places=2)
    
class ActividadRepositorioForm(forms.ModelForm):
    class Meta:
        model = ActividadRepositorio
        fields = ['periodo', 'anio_ingreso', 'anio_egreso', 'numero_acta', 'nota_aprobacion']


class ActividadFilterForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=False, label='Nombre')
    modalidad = forms.ModelChoiceField(queryset=Modalidad.objects.all(), required=False, label='Modalidad')
    fecha = forms.DateField(required=False, label='Fecha', widget=forms.DateInput(attrs={'type': 'date'}))