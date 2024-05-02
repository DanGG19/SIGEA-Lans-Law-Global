from django.urls import path
from SIGEA_APP import views


urlpatterns = [
    path('', views.index, name="index"),
]
