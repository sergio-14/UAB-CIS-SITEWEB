from django import forms
from .models import InvCientifica, ComentarioInvCientifica, InvSettings, PerfilProyecto, ComentarioPerfil, ActividadRepositorio

# área de investigación científica 
class InvCientificaForm(forms.ModelForm):
    class Meta:
        model = InvCientifica
        fields = ['invtitulo', 'invdescripcion', 'invdocumentacion', 'invmodalidad', 'invdestacado']
        widgets = {
            'invdescripcion': forms.Textarea(attrs={'class': 'descripcion-field'}),
        }

class InvComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioInvCientifica
        fields = ['invcomentario'] 
        widgets = {
            'invcomentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }

class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = InvSettings
        fields = ['habilitarInv']

    def __init__(self, *args, **kwargs):
        super(GlobalSettingsForm, self).__init__(*args, **kwargs)
        
# área de perfil de proyecto 
class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilProyecto
        fields = ['pertitulo', 'perdescripcion', 'perdocumentacion', 'permodalidad']
        widgets = {
            'perdescripcion': forms.Textarea(attrs={'class': 'descripcion-field'}),
        }
        
class PerComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioPerfil
        fields = ['percomentario'] 
        widgets = {
            'percomentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }



from .models import ActividadControl

class ActividadControlForm(forms.ModelForm):
    class Meta:
        model = ActividadControl
        fields = ['estudiante', 'tutor', 'jurado_1', 'jurado_2', 'jurado_3']
        
from .models import Actividad

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['estudiante', 'tutor', 'jurado_1', 'jurado_2', 'jurado_3', 'titulo', 'resumen', 'modalidad', 'guia_externo', 'documentacion']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'tutor': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'jurado_1': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'jurado_2': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'jurado_3': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'modalidad': forms.Select(attrs={'class': 'form-control'}),
            'guia_externo': forms.TextInput(attrs={'class': 'form-control'}),
            'documentacion': forms.FileInput(attrs={'class': 'form-control-file'}),
        }



from .models import Comentarioactividad
class ActComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentarioactividad
        fields = ['actcomentario'] 
        widgets = {
            'actcomentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }
        
import datetime

current_year = datetime.datetime.now().year
YEAR_CHOICES = [(year, year) for year in range(1990, current_year + 1)]

class TransferirActividadForm(forms.Form):
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
        fields = ['anio_ingreso', 'anio_egreso', 'numero_acta', 'nota_aprobacion']