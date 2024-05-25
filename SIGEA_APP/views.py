from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

@login_required
def index(request):
    if request.user.tipousuario == 1:
        return render(request, 'SIGEA_APP/admin/index.html')
    elif request.user.tipousuario == 2:
        return render(request, 'SIGEA_APP/secretaria/index.html')
    elif request.user.tipousuario == 3:
        return render(request, 'SIGEA_APP/abogado/index.html')

def login_V(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'registration/login.html', {'error_message': 'Datos Incorrectos'})
    return render(request, 'registration/login.html')

class UsuarioListView(ListView):
    model = Usuario
    template_name = 'SIGEA_APP/usuario_list.html'

class UsuarioDetailView(DetailView):
    model = Usuario
    template_name = 'SIGEA_APP/usuario_detail.html'

def usuario_create_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dui = request.POST.get('dui')
        telefono = request.POST.get('telefono')
        salario = request.POST.get('salario')
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipousuario = request.POST.get('tipousuario')
        idservicio = request.POST.get('idservicio')
        idplandes = request.POST.get('idplandes')

        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            dui=dui,
            telefono=telefono,
            salario=salario,
            email=email,
            password=password,
            tipousuario=tipousuario,
            idservicio_id=idservicio,
            idplandes_id=idplandes,
        )
        usuario.save()
        return redirect('usuario_list')
    return render(request, 'SIGEA_APP/usuario_form.html')

def usuario_update_view(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre')
        usuario.apellido = request.POST.get('apellido')
        usuario.dui = request.POST.get('dui')
        usuario.telefono = request.POST.get('telefono')
        usuario.salario = request.POST.get('salario')
        usuario.email = request.POST.get('email')
        usuario.password = request.POST.get('password')
        usuario.tipousuario = request.POST.get('tipousuario')
        usuario.idservicio_id = request.POST.get('idservicio')
        usuario.idplandes_id = request.POST.get('idplandes')
        usuario.save()
        return redirect('usuario_list')
    return render(request, 'SIGEA_APP/usuario_form.html', {'usuario': usuario})

def usuario_delete_view(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuario_list')
    return render(request, 'SIGEA_APP/usuario_confirm_delete.html', {'usuario': usuario})
