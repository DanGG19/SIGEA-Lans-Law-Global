from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"), #Ruta para la página de inicio, que llama a la vista index.
    path('login/', views.login_V, name="login"), #Ruta para la página de inicio de sesión, que llama a la vista login_V.
    path('accounts/login/', views.login_V, name="login"), #Ruta para la redirección de inicio de sesión (usualmente usada por el sistema de autenticación de Django).
    path('usuario/', views.usuario_list, name='usuario_list'), #Ruta para listar los usuarios, que llama a la vista usuario_list.
    path('usuario/create/', views.usuario_create, name='usuario_create'), #Ruta para crear un usuario, que llama a la vista usuario_create.
    path('usuario/update/<int:idusuario>/', views.usuario_update, name='usuario_update'),  # Ruta para actualizar un usuario, que llama a la vista usuario_update.
    path('usuario/delete/<int:idusuario>/', views.usuario_delete, name='usuario_delete'),  # Ruta para eliminar un usuario, que llama a la vista usuario_delete.
    path('usuario/detail/<int:idusuario>/', views.usuario_detail, name='usuario_detail'),  # Ruta para ver los detalles de un usuario, que llama a la vista usuario_detail.
]
