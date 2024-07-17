from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403
from repositoriotitulados import views
from .views import TransferirActividadView

urlpatterns = [   
                
    path('admrepositorio/transferir_actividad/<int:actividad_id>/', TransferirActividadView.as_view(), name='transferir_actividad'),
    path('admrepositorio/listarepositorios/', views.listarepositorios, name='listarepositorios'),
    path('admrepositorio/listaractividadesaprovadas/', views.listaractividadesaprovadas, name='listaractividadesaprovadas'),
    path('admrepositorio/actividad_repositorio/<int:pk>/editar/', views.editar_actividad_repositorio, name='editar_actividad_repositorio'),
    
    path('repositoriopublico/actividades/', views.actividad_list, name='actividad_list'),
]
#handler403 = handle_permission_denied