from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date
from django.conf import settings
from django.core.exceptions import ValidationError  

User = get_user_model()

ESTADO_CHOICES = [
    ('Aprobado', 'Aprobado'),
    ('Pendiente', 'Pendiente'),
    ('Rechazado', 'Rechazado'),
]

#class TutorExterno(models.Model):
#    nombre = models.CharField(max_length=100)
#   apellido = models.CharField(max_length=100)
#
#    def __str__(self):
#        return f"{self.nombre} {self.apellido}"

#class Materia(models.Model):
#    sigla = models.CharField(max_length=10)
#    nombre = models.CharField(max_length=100)
#    plan = models.CharField(max_length=100)
#
#    def __str__(self):
#        return f"{self.nombre} ({self.sigla})"

class Modalidad(models.Model):
    nombre = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nombre

class InvCientifica(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario relacionado')
    invtitulo = models.CharField(max_length=150, verbose_name='Agregar Titulo')
    slug = models.SlugField(unique=True)
    invfecha_creacion = models.DateTimeField(auto_now_add=True)
    invdescripcion = models.TextField(verbose_name='Agregar una Descripcion', blank=True)
    invdocumentacion = models.FileField(upload_to='documento/proyecto', verbose_name='Agregar Documentacion', null=True, blank=True)
    invmodalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, verbose_name='Seleccione Una Modalidad')
    invdestacado = models.BooleanField(default=True, verbose_name='Destacar Formulario')
    investado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return self.invtitulo

class ComentarioInvCientifica(models.Model):
    invcomentario = models.TextField(max_length=1000, help_text='', verbose_name='Ingrese Comentario Retroalimentativo')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    invfecha_post = models.DateTimeField(auto_now_add=True)
    invproyecto_relacionado = models.ForeignKey(InvCientifica, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-invfecha_post']

    def __str__(self):
        return self.invcomentario[:15] + '...' if len(self.invcomentario) > 15 else self.invcomentario

class InvSettings(models.Model):
    habilitarInv = models.BooleanField(default=True, verbose_name='Habilitar Formulario')

    def __str__(self):
        return "Configuración Global"

class PerfilProyecto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario relacionado')
    pertitulo = models.CharField(max_length=150, verbose_name='Agregar Titulo Perfil')
    slug = models.SlugField(unique=True)
    perfecha_creacion = models.DateTimeField(auto_now_add=True)
    perdescripcion = models.TextField(verbose_name='Agregar una Descripcion', blank=True)
    perdocumentacion = models.FileField(upload_to='documento/proyecto', verbose_name='Agregar Documentacion', null=True, blank=True)
    permodalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, verbose_name='Seleccione Una Modalidad')
    perestado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return self.pertitulo

class ComentarioPerfil(models.Model):
    percomentario = models.TextField(max_length=1000, help_text='', verbose_name='Ingrese Comentario Retroalimentativo')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    perfecha_post = models.DateTimeField(auto_now_add=True)
    perproyecto_relacionado = models.ForeignKey(PerfilProyecto, on_delete=models.CASCADE, related_name='comentarios')

    class Meta:
        ordering = ['-perfecha_post']

    def __str__(self):
        return self.percomentario[:15] + '...' if len(self.percomentario) > 15 else self.percomentario
    
####################################

class ActividadControl(models.Model):
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividad_estudiante', on_delete=models.CASCADE)
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividad_tutor', on_delete=models.CASCADE)
    jurado_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividad_jurado_1', on_delete=models.CASCADE)
    jurado_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividad_jurado_2', on_delete=models.CASCADE)
    jurado_3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividad_jurado_3', on_delete=models.CASCADE)

    def habilitar_actividad(self):
        actividad, created = Actividad.objects.get_or_create(
            estudiante=self.estudiante,
            defaults={
                'tutor': self.tutor,
                'jurado_1': self.jurado_1,
                'jurado_2': self.jurado_2,
                'jurado_3': self.jurado_3,
                'habilitada': True
            }
        )
        if not created:
            actividad.tutor = self.tutor
            actividad.jurado_1 = self.jurado_1
            actividad.jurado_2 = self.jurado_2
            actividad.jurado_3 = self.jurado_3
            actividad.habilitada = True
            actividad.save()
        return actividad

    def __str__(self):
        return f"ActividadControl for {self.estudiante}"

class Actividad(models.Model):
    estudiante = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividades_estudiante', on_delete=models.CASCADE)
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividades_tutor', on_delete=models.CASCADE)
    jurado_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividades_jurado_1', on_delete=models.CASCADE)
    jurado_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividades_jurado_2', on_delete=models.CASCADE)
    jurado_3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actividades_jurado_3', on_delete=models.CASCADE)
    habilitada = models.BooleanField(default=False)
    titulo = models.CharField(max_length=100, default='------')
    resumen = models.TextField(max_length=500, default='Describa el Proyecto...')
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE, default=1, verbose_name='Seleccione Una Modalidad')
    fecha = models.DateField(default=timezone.now)
    guia_externo = models.CharField(max_length=250, default='-----------')
    documentacion = models.FileField(upload_to='documento/proyecto', verbose_name='Agregar Documentacion', null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    jurado_1_aprobado = models.BooleanField(default=False)
    jurado_2_aprobado = models.BooleanField(default=False)
    jurado_3_aprobado = models.BooleanField(default=False)

    def __str__(self):
        return f"Actividad for {self.estudiante}"
    
    def save(self, *args, **kwargs):
        if self.estado in ['Aprobada', 'Rechazada']:
            # Verificar que todos los jurados han aprobado
            if not (self.jurado_1_aprobado and self.jurado_2_aprobado and self.jurado_3_aprobado):
                raise ValidationError("No se puede cambiar el estado sin la aprobación de todos los jurados.")
        
        super().save(*args, **kwargs)
    
class Comentarioactividad(models.Model):
    actcomentario = models.TextField(max_length=1000, help_text='', verbose_name='Ingrese Comentario Retroalimentativo')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    actfecha_post = models.DateTimeField(auto_now_add=True)
    actproyecto_relacionado = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='comentarios')

    class Meta:
        ordering = ['-actfecha_post']

    def __str__(self):
        return self.actcomentario[:15] + '...' if len(self.actcomentario) > 15 else self.actcomentario


