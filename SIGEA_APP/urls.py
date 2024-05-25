from django.urls import include, path
from SIGEA_APP import views


urlpatterns = [
    path('', views.index, name="index"),#This is the default page, recordar que se debe llamar el nombre name="index" para las referencias
    path('login/', views.login_V, name="login"), #This is the login page, recordar que se debe llamar al nombre name="login" para las referencias
    path('accounts/login/', views.login_V, name="login"), #Esto ya existe en Django, es una carpeta ya está implemantada, aunque no se vea en el proyecto de Django para redirigir al login
]
