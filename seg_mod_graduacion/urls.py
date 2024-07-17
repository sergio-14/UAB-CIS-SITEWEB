from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403
from .views import handle_permission_denied
from seg_mod_graduacion import views
urlpatterns = [    
    #segguimiento modalidad de graduacion investigacion cientifica
    path('invcientifica/agregar_investigacion/', views.agregar_investigacion, name='agregar_investigacion'),
    path('invcientifica/vista_investigacion/',views.vista_investigacion, name='vista_investigacion'),
    path('invcientifica/ProyectosParaAprobar/', views.ProyectosParaAprobar.as_view(), name='ProyectosParaAprobar'),
    path('AprobarProyecto/<int:proyecto_id>/', views.AprobarProyecto.as_view(), name='AprobarProyecto'),
    path('RechazarProyecto/<int:proyecto_id>/', views.RechazarProyecto.as_view(), name='RechazarProyecto'),
    path('invcientifica/global_settings/', views.global_settings_view, name='global_settings'),
    
    #seguimiento modalidad de graduacion perfil de proyecto
    path('perfil/agregar_perfil/', views.agregar_perfil, name='agregar_perfil'),
    path('perfil/vista_perfil/',views.vista_perfil, name='vista_perfil'),
    path('perfil/PerfilesParaAprobar/', views.PerfilesParaAprobar.as_view(), name='PerfilesParaAprobar'),
    path('AprobarPerfil/<int:proyecto_id>/', views.AprobarPerfil.as_view(), name='AprobarPerfil'),
    path('RechazarPerfil/<int:proyecto_id>/', views.RechazarPerfil.as_view(), name='RechazarPerfil'),

    #seguimiento modalidad de graduacion proyecto final
    path('controlador/actividad_control/nueva/', views.crear_actividad_control, name='crear_actividad_control'),
    path('controlador/editar_actividad_control/<int:pk>/editar/', views.editar_actividad_control, name='editar_actividad_control'),
    path('controlador/lista_actividad_control/', views.lista_actividad_control, name='lista_actividad_control'),
    
    path('proyectofinal/revision/<int:actividad_id>/', views.revisar_actividad, name='revisar_actividad'),
    path('controlador/revision/<int:actividad_id>/', views.revision, name='revision'),
    path('controlador/listaactividades/', views.listaactividades, name='listaactividades'),
    
    path('proyectofinal/crear_actividad/nueva/', views.crear_actividad, name='crear_actividad'),
    path('proyectofinal/actividad/', views.lista_actividad, name='lista_actividad'),
]
handler403 = handle_permission_denied