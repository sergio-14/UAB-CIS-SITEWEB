from django.shortcuts import render
from seg_mod_graduacion.models import ActividadRepositorio, Actividad

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

# Create your views here.

from django.urls import reverse
from .forms import TransferirActividadForm, ActividadRepositorioForm

class TransferirActividadView(View):
    def get(self, request, actividad_id):
        actividad = get_object_or_404(Actividad, id=actividad_id, estado='Aprobado')
        form = TransferirActividadForm()
        return render(request, 'admrepositorio/transferir_actividad.html', {'form': form, 'actividad': actividad})

    def post(self, request, actividad_id):
        actividad = get_object_or_404(Actividad, id=actividad_id, estado='Aprobado')
        form = TransferirActividadForm(request.POST)
        if form.is_valid():
            anio_ingreso = form.cleaned_data['anio_ingreso']
            anio_egreso = form.cleaned_data['anio_egreso']
            numero_acta = form.cleaned_data['numero_acta']
            nota_aprobacion = form.cleaned_data['nota_aprobacion']
            # Asegúrate de que todos los argumentos son proporcionados aquí
            actividad.transferir_a_repositorio(
                form.cleaned_data['periodo'],  # Añadido aquí el argumento 'periodo'
                anio_ingreso,
                anio_egreso,
                numero_acta,
                nota_aprobacion
                )
            return redirect('dashboard')
        return render(request, 'admrepositorio/transferir_actividad.html', {'form': form, 'actividad': actividad})
    
    
    
def listaractividadesaprovadas(request):
    # Obtén todos los IDs de estudiantes que ya tienen un ActividadRepositorio
    repositorios_existentes = ActividadRepositorio.objects.values_list('estudiante_id', flat=True)
    
    # Filtra las actividades aprobadas, excluyendo aquellas donde el estudiante ya tiene un repositorio
    actividades_aprobadas = Actividad.objects.filter(
        estado='Aprobado'
    ).exclude(
        estudiante_id__in=repositorios_existentes
    )
    
    return render(request, 'admrepositorio/listaractividadesaprovadas.html', {'acti': actividades_aprobadas})


#def listarepositorios(request):
#    actividades_repositorio = ActividadRepositorio.objects.all()
#   return render(request, 'admrepositorio/listarepositorios.html', {'actirepositorio': actividades_repositorio})

def listarepositorios(request):
    # Filtrado por nombre del estudiante
    query = request.GET.get('q')
    if query:
        actividades_repositorio = ActividadRepositorio.objects.filter(estudiante__nombre__icontains=query)
    else:
        actividades_repositorio = ActividadRepositorio.objects.all()

    # Paginación
    paginator = Paginator(actividades_repositorio, 4)  # 4 elementos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'actirepositorio': page_obj,
        'query': query,  # Pasar la consulta al contexto para mantener el valor en el formulario de búsqueda
    }
    return render(request, 'admrepositorio/listarepositorios.html', context)


def editar_actividad_repositorio(request, pk):
    actividad = get_object_or_404(ActividadRepositorio, pk=pk)
    
    if request.method == 'POST':
        form = ActividadRepositorioForm(request.POST, instance=actividad)
        if form.is_valid():
            form.save()
            return redirect('listarepositorios')
    else:
        form = ActividadRepositorioForm(instance=actividad)
    
    return render(request, 'admrepositorio/editar_actividad_repositorio.html', {'form': form, 'actividad': actividad})


#Repositorio publico
from .forms import ActividadFilterForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


def actividad_list(request):
    actividades = ActividadRepositorio.objects.all()
    form = ActividadFilterForm(request.GET)

    if form.is_valid():
        nombre_completo = form.cleaned_data.get('nombre_completo')
        modalidad = form.cleaned_data.get('modalidad')
        periodo = form.cleaned_data.get('periodo')

        if nombre_completo:
            nombres = nombre_completo.split()
            if len(nombres) == 2:
                nombre, apellido = nombres
                actividades = actividades.filter(Q(estudiante__nombre__icontains=nombre) & Q(estudiante__apellido__icontains=apellido))
            else:
                actividades = actividades.filter(
                    Q(estudiante__nombre__icontains=nombre_completo) |
                    Q(estudiante__apellido__icontains=nombre_completo)
                )
        if modalidad:
            actividades = actividades.filter(modalidad=modalidad)
        if periodo:
            actividades = actividades.filter(periodo=periodo)

    paginator = Paginator(actividades, 15)  
    page_number = request.GET.get('page')
    try:
        actividades_paginated = paginator.page(page_number)
    except PageNotAnInteger:
        actividades_paginated = paginator.page(1)
    except EmptyPage:
        actividades_paginated = paginator.page(paginator.num_pages)

    return render(request, 'repositoriopublico/actividad_list.html', {'form': form, 'actividades': actividades_paginated})

from .forms import AgregarForm

def agregar_actividad_repositorio(request):
    if request.method == 'POST':
        form = AgregarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('listarepositorios'))
        else:
            print(form.errors)
    else:
        form = AgregarForm()
    
    return render(request, 'admrepositorio/agregar_actividad_repositorio.html', {'form': form})