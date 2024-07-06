from django.contrib import admin
from .models import InvCientifica, Modalidad, ComentarioInvCientifica, ComentarioPerfil, InvSettings, PerfilProyecto

from .models import Actividad, ActividadControl,Comentarioactividad

admin.site.register(Actividad)
admin.site.register(ActividadControl)

# Registra tus modelos aquí
admin.site.register(InvCientifica)
admin.site.register(Modalidad)
admin.site.register(ComentarioInvCientifica)
admin.site.register(ComentarioPerfil)
admin.site.register(InvSettings)
admin.site.register(PerfilProyecto)
admin.site.register(Comentarioactividad)