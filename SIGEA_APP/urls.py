from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_V, name="login"),
    path('accounts/login/', views.login_V, name="login"),
    path('usuario/', views.usuario_list, name='usuario_list'),
    path('usuario/create/', views.usuario_create, name='usuario_create'),
    path('usuario/update/<int:idusuario>/', views.usuario_update, name='usuario_update'),  # Actualizar aquí
    path('usuario/delete/<int:idusuario>/', views.usuario_delete, name='usuario_delete'),  # Actualizar aquí
    path('usuario/detail/<int:idusuario>/', views.usuario_detail, name='usuario_detail'),  # Actualizar aquí
]
