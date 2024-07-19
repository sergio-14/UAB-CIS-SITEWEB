from django import forms
from django.contrib.auth.models import Group
from gestion_usuarios.models import User 
from .models import InvCientifica, ComentarioInvCientifica, InvSettings, PerfilProyecto, ComentarioPerfil, ActividadRepositorio

# área de investigación científica 
class InvCientificaForm(forms.ModelForm):
    class Meta:
        model = InvCientifica
        fields = ['invtitulo', 'invdescripcion', 'invdocumentacion']
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
        fields = ['estudiante', 'tutor', 'jurado_1', 'jurado_2', 'jurado_3','modalidad']
        labels = {
            'estudiante': 'Seleccione el Postulante',
            'tutor': 'Seleccione al Tutor Designado',
            'jurado_1': 'Seleccione al Primero Tribumal Designado',
            'jurado_2': 'Seleccione al Segundo Tribumal Designado',
            'jurado_3': 'Seleccione al Tercer Tribumal Designado',
            'modalidad': 'Seleccione modalidad ',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        estudiantes_group = Group.objects.get(name="Estudiantes")
        docentes_group = Group.objects.get(name="Docentes")
        # Obtiene los IDs de los usuarios que ya tienen una actividad asignada
        usuarios_con_actividad = ActividadControl.objects.values_list('estudiante', flat=True)
        # Filtra los usuarios del grupo "Estudiantes" que no tienen una actividad asignada
        self.fields['estudiante'].queryset = User.objects.filter(
            groups=estudiantes_group
        ).exclude(id__in=usuarios_con_actividad)
        # Filtra los usuarios del grupo "Docentes"
        self.fields['tutor'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_1'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_2'].queryset = User.objects.filter(groups=docentes_group)
        self.fields['jurado_3'].queryset = User.objects.filter(groups=docentes_group)
        
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
            'modalidad': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
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
        
