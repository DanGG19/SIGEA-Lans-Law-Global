from django.urls import path
from SIGEA import settings
from SIGEA_APP import views 
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"), #Ruta para la página de inicio, que llama a la vista index.
    path('login/', views.login_V, name="login"), #Ruta para la página de inicio de sesión, que llama a la vista login_V.
    path('accounts/login/', views.login_V, name="login"), #Ruta para la redirección de inicio de sesión (usualmente usada por el sistema de autenticación de Django).
    path('usuario/', views.usuario_list, name='usuario_list'), #Ruta para listar los usuarios, que llama a la vista usuario_list.
    path('usuario/create/', views.usuario_create, name='usuario_create'), #Ruta para crear un usuario, que llama a la vista usuario_create.
    path('usuario/update/<int:idusuario>/', views.usuario_update, name='usuario_update'),  # Ruta para actualizar un usuario, que llama a la vista usuario_update.
    path('usuario/delete/<int:idusuario>/', views.usuario_delete, name='usuario_delete'),  # Ruta para eliminar un usuario, que llama a la vista usuario_delete.
    path('usuario/detail/<int:idusuario>/', views.usuario_detail, name='usuario_detail'),  # Ruta para ver los detalles de un usuario, que llama a la vista usuario_detail.
    path('departamento/', views.departamento_list, name='departamento_list'),
    path('departamento/create/', views.departamento_create, name='departamento_create'), #Ruta para crear un usuario, que llama a la vista usuario_create.
    path('departamento/update/<int:iddepartamento>/', views.departamento_update, name='departamento_update'),  # Ruta para actualizar un usuario, que llama a la vista usuario_update.
    path('departamento/delete/<int:iddepartamento>/', views.departamento_delete, name='departamento_delete'),  # Ruta para eliminar un usuario, que llama a la vista usuario_delete.
    path('departamento/detail/<int:iddepartamento>/', views.departameto_detail, name='departamento_detail'),  # Ruta para ver los detalles de un usuario, que llama a la vista usuario_detail.
    path('servicio/', views.servicio_list, name='servicio_list'),
    path('servicio/create/', views.servicio_create, name='servicio_create'), #Ruta para crear un usuario, que llama a la vista usuario_create.
    path('servicio/update/<int:idservicio>/', views.servicio_update, name='servicio_update'),  # Ruta para actualizar un usuario, que llama a la vista usuario_update.
    path('servicio/delete/<int:idservicio>/', views.servicio_delete, name='servicio_delete'),  # Ruta para eliminar un usuario, que llama a la vista usuario_delete.
    path('servicio/detail/<int:idservicio>/', views.servicio_detail, name='servicio_detail'),  # Ruta para ver los detalles de un usuario, que llama a la vista usuario_detail.
    path('actividades', views.actividades, name='actividades'),
    path('actividades/create', views.actividades_create, name='actividades_create'),
    path('actividades/list', views.actividades_list, name='actividades_list'),
    path('actividades/delete/<int:idactividad>/', views.actividad_delete, name='actividad_delete'),
    path('recordatorio/create', views.recordatorio_create, name='recordatorio_create'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)