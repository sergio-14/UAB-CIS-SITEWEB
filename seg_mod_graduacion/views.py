from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

from .forms import InvCientificaForm, InvComentarioForm, GlobalSettingsForm, PerfilForm, PerComentarioForm, ActComentarioForm
from .models import InvCientifica, ComentarioInvCientifica, InvSettings, PerfilProyecto, ComentarioPerfil, Comentarioactividad

##############  permisos decoradores  para funciones y clases   ################  

#modalidad de graduación permigroup 
def permiso_M_G(user, ADMMGS):
    try:
        grupo = Group.objects.get(name=ADMMGS)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{ADMMGS}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied
    
#permiso para docentes  
def permiso_Docentes(user, Docentes):
    try:
        grupo = Group.objects.get(name=Docentes)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{Docentes}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied

#permiso para estudiantes
def permiso_Estudiantes(user, Estudiantes):
    try:
        grupo = Group.objects.get(name=Estudiantes)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{Estudiantes}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied

#vista 403
def handle_permission_denied(request, exception):
    return render(request, '403.html', status=403)

################  vistas modalidad de graduación  ##########################

#vista agregar formulario alcance de proyecto 
@login_required
@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes')) 
def vista_investigacion(request):
    proyectos_usuario = InvCientifica.objects.filter(user=request.user).order_by('-invfecha_creacion').prefetch_related('comentarioinvcientifica_set')

    paginator = Paginator(proyectos_usuario, 1)  
    page_number = request.GET.get('page')
    proyectos_paginados = paginator.get_page(page_number)

    return render(request, 'invcientifica/vista_investigacion.html', {'proyectos': proyectos_paginados})

@method_decorator(user_passes_test(lambda u: permiso_M_G(u, 'ADMMGS')), name='dispatch')
class ProyectosParaAprobar(View):
    def get(self, request):
        proyectos = InvCientifica.objects.filter(investado='Pendiente')
        proyectos_con_formulario = {proyecto: InvComentarioForm() for proyecto in proyectos}
        
        context = {
            'proyectos': proyectos_con_formulario,
        }
        return render(request, 'invcientifica/ProyectosParaAprobar.html', context)
    
    def post(self, request):
        proyecto_id = request.POST.get('proyecto_id')
        comentario_texto = request.POST.get('comentario_texto')
        if proyecto_id and comentario_texto:
            proyecto = get_object_or_404(InvCientifica, pk=proyecto_id)
            ComentarioInvCientifica.objects.create(invcomentario=comentario_texto, user=request.user, invproyecto_relacionado=proyecto)
            messages.success(request, 'Comentario agregado exitosamente.')
        else:
            messages.error(request, 'Hubo un error al agregar el comentario.')
        
        if 'aprobar' in request.POST:
            return AprobarProyecto().post(request, proyecto_id)
        elif 'rechazar' in request.POST:
            return RechazarProyecto().post(request, proyecto_id)
        else:
            messages.error(request, 'Hubo un error al procesar la solicitud.')
            return redirect('ProyectosParaAprobar')

class AprobarProyecto(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(InvCientifica, pk=proyecto_id)
        proyecto.investado = 'Aprobado'
        proyecto.save()
        messages.success(request, '¡Proyecto aprobado exitosamente!')
        return redirect('ProyectosParaAprobar')

class RechazarProyecto(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(InvCientifica, pk=proyecto_id)
        proyecto.investado = 'Rechazado'
        proyecto.save()
        messages.error(request, '¡Proyecto rechazado!')
        return redirect('ProyectosParaAprobar')

@user_passes_test(lambda u: permiso_M_G(u, 'ADMMGS')) 
def global_settings_view(request):
    settings = InvSettings.objects.first()
    if not settings:
        settings = InvSettings()

    if request.method == 'POST':
        form = GlobalSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = GlobalSettingsForm(instance=settings)
    
    return render(request, 'invcientifica/global_settings.html', {'form': form, 'settings': settings})

@login_required
@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes')) 
def agregar_investigacion(request):
    settings = InvSettings.objects.first()
    
    if not settings:
        messages.error(request, 'No se encontró la configuración global. Por favor, contacta al administrador.')
        return redirect('global_settings')
    
    tiene_investigacion_aprobada = InvCientifica.objects.filter(user=request.user, investado='Aprobado').exists()
    
    form_disabled = not settings.habilitarInv or tiene_investigacion_aprobada
    
    if request.method == 'POST' and not form_disabled:
        form = InvCientificaForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            
            slug = slugify(proyecto.invtitulo)
            counter = 1
            while InvCientifica.objects.filter(slug=slug).exists():
                slug = f"{slug}-{counter}"
                counter += 1
            proyecto.slug = slug
            
            proyecto.user = request.user
            proyecto.save()
            return redirect('dashboard')
    else:
        form = InvCientificaForm()
    
    if form_disabled:
        for field in form.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
    
    return render(request, 'invcientifica/agregar_investigacion.html', {
        'form': form,
        'form_disabled': form_disabled,
    })

########  PERFIL DE PROYECTO M. G 2DA PARTE   #########
@login_required
@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes')) 
def vista_perfil(request):
    proyectos_usuario = PerfilProyecto.objects.filter(user=request.user).order_by('-perfecha_creacion').prefetch_related('comentarios')
    
    paginator = Paginator(proyectos_usuario, 1) 
    page_number = request.GET.get('page')
    proyectos_paginados = paginator.get_page(page_number)

    return render(request, 'perfil/vista_perfil.html', {'proyectos': proyectos_paginados})

@method_decorator(user_passes_test(lambda u: permiso_M_G(u, 'ADMMGS')), name='dispatch')
class PerfilesParaAprobar(View):
    def get(self, request):
        proyectos = PerfilProyecto.objects.filter(perestado='Pendiente')
        proyectos_con_formulario = {proyecto: PerComentarioForm() for proyecto in proyectos}
        
        context = {
            'proyectos': proyectos_con_formulario,
        }
        return render(request, 'perfil/PerfilesParaAprobar.html', context)
    
    def post(self, request):
        proyecto_id = request.POST.get('proyecto_id')
        comentario_texto = request.POST.get('comentario_texto')
        if proyecto_id and comentario_texto:
            proyecto = get_object_or_404(PerfilProyecto, pk=proyecto_id)
            ComentarioPerfil.objects.create(percomentario=comentario_texto, user=request.user, perproyecto_relacionado=proyecto)
            messages.success(request, 'Comentario agregado exitosamente.')
        else:
            messages.error(request, 'Hubo un error al agregar el comentario.')
        
        if 'aprobar' in request.POST:
            return AprobarPerfil().post(request, proyecto_id)
        elif 'rechazar' in request.POST:
            return RechazarPerfil().post(request, proyecto_id)
        else:
            messages.error(request, 'Hubo un error al procesar la solicitud.')
            return redirect('PerfilesParaAprobar')
    
class AprobarPerfil(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(PerfilProyecto, pk=proyecto_id)
        proyecto.perestado = 'Aprobado'
        proyecto.save()
        messages.success(request, '¡Perfil aprobado exitosamente!')
        return redirect('PerfilesParaAprobar')

class RechazarPerfil(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(PerfilProyecto, pk=proyecto_id)
        proyecto.perestado = 'Rechazado'
        proyecto.save()
        messages.error(request, '¡Perfil rechazado!')
        return redirect('PerfilesParaAprobar')

@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes'))
def agregar_perfil(request):
    tiene_investigacion_aprobada = InvCientifica.objects.filter(user=request.user, investado='Aprobado').exists()
    form_disabled = not tiene_investigacion_aprobada

    if request.method == 'POST' and not form_disabled:
        formp = PerfilForm(request.POST, request.FILES)
        print("Formulario enviado. Método POST.")
        if formp.is_valid():
            print("Formulario es válido.")
            proyecto = formp.save(commit=False)
            
            slug = slugify(proyecto.pertitulo)
            counter = 1
            while PerfilProyecto.objects.filter(slug=slug).exists():
                slug = f"{slug}-{counter}"
                counter += 1
            proyecto.slug = slug
            
            proyecto.user = request.user
            proyecto.save()
            return redirect('dashboard')
        else:
            print("Formulario no es válido:", formp.errors)
    else:
        formp = PerfilForm()

    if form_disabled:
        for field in formp.fields.values():
            field.widget.attrs['disabled'] = 'disabled'

    return render(request, 'perfil/agregar_perfil.html', {
        'formp': formp,
        'form_disabled': form_disabled,
    })
    
#### VISTA DE PROYECTO FINAL #####

### VISTA PARA EL ESTUDIANTE ###
###############################################################


from .models import ActividadControl
from .forms import ActividadControlForm

#controlador de proyecto final
def crear_actividad_control(request):
    if request.method == 'POST':
        form = ActividadControlForm(request.POST)
        if form.is_valid():
            actividad_control = form.save()
            actividad_control.habilitar_actividad()
            return redirect('dashboard') 
    else:
        form = ActividadControlForm()
    
    return render(request, 'controlador/crear_actividad_control.html', {'form': form})

#lista de agregacion y proyectos finales
@login_required
def lista_actividad_control(request):
    actividades_control = ActividadControl.objects.all().distinct()
    for actividad in actividades_control:
        print(actividad.estudiante)

    return render(request, 'controlador/lista_actividad_control.html', {'actividades_control': actividades_control})

@login_required
def editar_actividad_control(request, pk):
    actividad_control = get_object_or_404(ActividadControl, pk=pk)

    if request.method == 'POST':
        form = ActividadControlForm(request.POST, instance=actividad_control)
        if form.is_valid():
            form.save()
            return redirect('lista_actividad_control')
    else:
        form = ActividadControlForm(instance=actividad_control)

    return render(request, 'controlador/editar_actividad_control.html', {'form': form})

from .models import Actividad
from django.utils import timezone
from .forms import ActividadForm

@login_required
def crear_actividad(request):
    estudiante = request.user
    actividad = None
    form = None

    try:
        actividad = Actividad.objects.get(estudiante=estudiante)
    except Actividad.DoesNotExist:
        actividad = None

    if actividad and actividad.habilitada:
        if request.method == 'POST':
            form = ActividadForm(request.POST, request.FILES, instance=actividad)
            if form.is_valid():
                actividad = form.save(commit=False)
                actividad.fecha = timezone.now()
                actividad.estado = 'Pendiente'  # Puedes ajustar este valor según sea necesario
                actividad.save()
                return redirect('dashboard')
        else:
            form = ActividadForm(instance=actividad)
    else:
        form = ActividadForm()  # or set form to None if no form is required in the template

    return render(request, 'proyectofinal/crear_actividad.html', {'form': form, 'actividad': actividad})


def lista_actividad(request):
    user = request.user
    actividades = Actividad.objects.filter(estudiante=user).prefetch_related('comentarios').order_by('-fecha')
    return render(request, 'proyectofinal/lista_actividad.html', {'actividades': actividades})

from .models import Comentarioactividad

@login_required
def revisar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, pk=actividad_id)
    user = request.user

    if request.method == 'POST':
        # Procesar el formulario de revisión y comentarios
        if user == actividad.jurado_1 and 'jurado_1_aprobado' in request.POST:
            actividad.jurado_1_aprobado = request.POST.get('jurado_1_aprobado') == 'on'

        if user == actividad.jurado_2 and 'jurado_2_aprobado' in request.POST:
            actividad.jurado_2_aprobado = request.POST.get('jurado_2_aprobado') == 'on'

        if user == actividad.jurado_3 and 'jurado_3_aprobado' in request.POST:
            actividad.jurado_3_aprobado = request.POST.get('jurado_3_aprobado') == 'on'

        # Guardar la actividad después de la revisión
        actividad.save()

        # Crear comentario si existe
        comentario_texto = request.POST.get('comentario_texto', '')
        if comentario_texto:
            comentario = Comentarioactividad(
                actcomentario=comentario_texto,
                user=request.user,
                actproyecto_relacionado=actividad
            )
            comentario.save()

        messages.success(request, 'Revisión de actividad y comentario guardados correctamente.')
        return redirect('listaactividades')

    return render(request, 'proyectofinal/revisar_actividad.html', {'actividad': actividad})


def listaactividades(request):
    actividades = Actividad.objects.all()
    return render(request, 'controlador/listaactividades.html', {'actividades': actividades})




@user_passes_test(lambda u: permiso_M_G(u, 'ADMMGS'))
def revision(request, actividad_id):
    actividad = get_object_or_404(Actividad, pk=actividad_id)
    user = request.user

    # Verificar que todos los jurados han aprobado antes de permitir cambiar el estado
    todos_aprobados = actividad.jurado_1_aprobado and actividad.jurado_2_aprobado and actividad.jurado_3_aprobado

    if request.method == 'POST':
        if 'cambiar_estado' in request.POST:
            if todos_aprobados:
                actividad.estado = 'Aprobado'
                actividad.save()
                messages.success(request, 'Estado de la actividad cambiado a Aprobado.')
            else:
                messages.error(request, 'Necesita que los 3 jurados aprueben la actividad para poder cambiar el estado.')
                
            return redirect('listaactividades')

    return render(request, 'controlador/revision.html', {'actividad': actividad, 'todos_aprobados': todos_aprobados})


