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
    



from gestion_usuarios.models import User 

class AgregarForm(forms.ModelForm):
    class Meta:
        model = ActividadRepositorio
        fields = [
            'estudiante', 'tutor', 'jurado_1', 'jurado_2', 'jurado_3', 
            'titulo', 'resumen', 'modalidad', 
            'guia_externo', 'documentacion', 'periodo', 'anio_ingreso', 
            'anio_egreso', 'numero_acta', 'nota_aprobacion'
        ]
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-select'}),
            'tutor': forms.Select(attrs={'class': 'form-select'}),
            'jurado_1': forms.Select(attrs={'class': 'form-select'}),
            'jurado_2': forms.Select(attrs={'class': 'form-select'}),
            'jurado_3': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.Textarea(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-select'}),
            'guia_externo': forms.TextInput(attrs={'class': 'form-control'}),
            'documentacion': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'periodo': forms.Select(attrs={'class': 'form-select'}),
            'anio_ingreso': forms.NumberInput(attrs={'class': 'form-control'}),
            'anio_egreso': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_acta': forms.TextInput(attrs={'class': 'form-control'}),
            'nota_aprobacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'estudiante': 'Nombre del Egresado:',
            'tutor': 'Tutor Asignado:',
            'jurado_1': 'Tribunal Asignado:',
            'jurado_2': 'Tribunal Asignado:',
            'jurado_3': 'Tribunal Asignado:',
            'titulo': 'Titulo de Proyecto:',
            'resumen': 'Descripción Breve del Proyecto:',
            'modalidad': 'Modalidad Optada:',
            'guia_externo': 'Tutor Externo:',
            'documentacion': 'Documentación Egresado:',
            'periodo': 'Periodo o Gestion:',
            'anio_ingreso': 'Año de Ingreso',
            'anio_egreso': 'Año de Egreso',
            'numero_acta': 'Número de Acta',
            'nota_aprobacion': 'Nota de Aprobación',
            'fecha': 'Fecha'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        estudiantes = User.objects.filter(groups__name='Estudiantes').exclude(repo_estudiante__isnull=False)
        self.fields['estudiante'].queryset = estudiantes

        docentes = User.objects.filter(groups__name='Docentes')
        self.fields['tutor'].queryset = docentes
        self.fields['jurado_1'].queryset = docentes
        self.fields['jurado_2'].queryset = docentes
        self.fields['jurado_3'].queryset = docentes
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.habilitada = True
        instance.jurado_1_aprobado = True
        instance.jurado_2_aprobado = True
        instance.jurado_3_aprobado = True
        instance.estado = 'Aprobado'
        if commit:
            instance.save()
        return instance