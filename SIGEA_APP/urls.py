from django.urls import path
from SIGEA_APP import views

urlpatterns = [
    path('', views.index, name="index"),  # Página de inicio
    path('login/', views.login_V, name="login"),  # Página de login
    path('accounts/login/', views.login_V, name="login"),  # Redirección a login
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),  # Listado de usuarios
    path('usuarios/nuevo/', views.usuario_create_view, name='usuario_create'),  # Crear usuario
    path('usuarios/<int:pk>/', views.UsuarioDetailView.as_view(), name='usuario_detail'),  # Detalle de usuario
    path('usuarios/<int:pk>/editar/', views.usuario_update_view, name='usuario_update'),  # Editar usuario
    path('usuarios/<int:pk>/eliminar/', views.usuario_delete_view, name='usuario_delete'),  # Eliminar usuario
]
