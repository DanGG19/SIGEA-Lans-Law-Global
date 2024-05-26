from django.shortcuts import render, get_object_or_404, redirect
from .models import Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import UsuarioForm

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
    return render(request, 'SIGEA_APP/registration/login.html')

@csrf_exempt
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_list.html', {'usuarios': usuarios})

@csrf_exempt
def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UsuarioForm()
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_form.html', {'form': form})

@csrf_exempt
def usuario_update(request, idusuario):  # Usamos idusuario aquí
    usuario = get_object_or_404(Usuario, idusuario=idusuario)  # y aquí también
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_form.html', {'form': form})

def usuario_detail(request, idusuario):  # Usamos idusuario aquí
    usuario = get_object_or_404(Usuario, idusuario=idusuario)  # y aquí también
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_detail.html', {'usuario': usuario})

@csrf_exempt
def usuario_delete(request, idusuario):  # Usamos idusuario aquí
    usuario = get_object_or_404(Usuario, idusuario=idusuario)  # y aquí también
    if request.method == 'POST':
        usuario.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
