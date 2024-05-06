from django.urls import path
from SIGEA_APP import views


urlpatterns = [
    path('', views.index, name="index"),#This is the default page, recordar que se debe llamar el nombre name="index" para las referencias
    path('login', views.login, name="login"),#This is the login page, recordar que se debe llamar al nombre name="login" para las referencias
]
