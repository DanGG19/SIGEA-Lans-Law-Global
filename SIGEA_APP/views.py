from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import *
from django.utils import timezone
from datetime import datetime

@login_required # Decorador para proteger la vista con login
def index(request): #Vista protegida por login que redirige al usuario a diferentes plantillas según su tipo de usuario (tipousuario).
    if request.user.tipousuario == 1: #Si el tipo de usuario es 1, se redirige al usuario a la plantilla de administrador.
        return render(request, 'SIGEA_APP/admin/index.html')
    elif request.user.tipousuario == 2: #Si el tipo de usuario es 2, se redirige al usuario a la plantilla de secretaria.
        return render(request, 'SIGEA_APP/secretaria/index.html')
    elif request.user.tipousuario == 3: #Si el tipo de usuario es 3, se redirige al usuario a la plantilla de abogado.
        return render(request, 'SIGEA_APP/abogado/index.html')

def login_V(request): #Vista para el inicio de sesión
    if request.method == 'POST': #Si el método es POST, se obtienen los datos del formulario y se autentica al usuario.
        email = request.POST['email'] #Se obtiene el email del formulario.
        password = request.POST['password'] #Se obtiene la contraseña del formulario.
        user = authenticate(request, username=email, password=password) #Se autentica al usuario con el email y la contraseña.
        if user is not None: #Si el usuario es autenticado, se inicia sesión y se redirige al usuario a la página de inicio.
            login(request, user) #Se inicia sesión.
            return redirect('index') #Se redirige al usuario a la página de inicio.
        else: #Si los datos son incorrectos, se muestra un mensaje de error.
            return render(request, 'registration/login.html', {'error_message': 'Datos Incorrectos'}) #Se muestra un mensaje de error.
    return render(request, 'registration/login.html') #Si el método no es POST, se muestra el formulario de inicio de sesión.

@csrf_exempt # Decorador para deshabilitar la protección CSRF
def usuario_list(request): #Vista para listar los usuarios
    usuarios = Usuario.objects.all() #Se obtienen todos los usuarios de la base de datos.
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_list.html', {'usuarios': usuarios}) #Se renderiza la plantilla usuario_list.html con los usuarios obtenidos.

@csrf_exempt # Decorador para deshabilitar la protección CSRF
def usuario_create(request): #Vista para crear un usuario
    if request.method == 'POST': #Si el método es POST, se crea un formulario con los datos del usuario.
        form = UsuarioForm(request.POST) #Se crea un formulario con los datos del usuario.
        if form.is_valid(): #Si el formulario es válido, se guarda el usuario en la base de datos.
            form.save() #Se guarda el usuario en la base de datos.
            return JsonResponse({'success': True}) #Se retorna un JSON con el mensaje de éxito.
        else:
            return JsonResponse({'success': False, 'errors': form.errors}) #Si el formulario no es válido, se retorna un JSON con el mensaje de error.
    else:
        form = UsuarioForm()
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_form.html', {'form': form}) #Si el método no es POST, se muestra el formulario para crear un usuario.

@csrf_exempt # Decorador para deshabilitar la protección CSRF
def usuario_update(request, idusuario): # Usamos idusuario aquí #Vista para actualizar un usuario
    usuario = get_object_or_404(Usuario, idusuario=idusuario) # y aquí también #Se obtiene el usuario a actualizar.
    if request.method == 'POST': #Si el método es POST, se crea un formulario con los datos del usuario.
        form = UsuarioForm(request.POST, instance=usuario) #Se crea un formulario con los datos del usuario.
        if form.is_valid():#Si el formulario es válido, se actualiza el usuario en la base de datos.
            form.save() #Se actualiza el usuario en la base de datos.
            return JsonResponse({'success': True}) #Se retorna un JSON con el mensaje de éxito.
        else:
            return JsonResponse({'success': False, 'errors': form.errors}) #Si el formulario no es válido, se retorna un JSON con el mensaje de error.
    else:
        form = UsuarioForm(instance=usuario) #Si el método no es POST, se muestra el formulario para actualizar un usuario.
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_form.html', {'form': form}) #Se renderiza la plantilla usuario_form.html con el formulario para actualizar un usuario.

def usuario_detail(request, idusuario):  # Usamos idusuario aquí #Vista para ver los detalles de un usuario
    usuario = get_object_or_404(Usuario, idusuario=idusuario)  # y aquí también #Se obtiene el usuario a mostrar.
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_detail.html', {'usuario': usuario}) #Se renderiza la plantilla usuario_detail.html con los datos del usuario.

@csrf_exempt # Decorador para deshabilitar la protección CSRF
def usuario_delete(request, idusuario):  # Usamos idusuario aquí #Vista para eliminar un usuario
    usuario = get_object_or_404(Usuario, idusuario=idusuario)  # y aquí también #Se obtiene el usuario a eliminar.
    if request.method == 'POST': #Si el método es POST, se elimina el usuario de la base de datos.
        usuario.delete() #Se elimina el usuario de la base de datos.
        return JsonResponse({'success': True}) #Se retorna un JSON con el mensaje de éxito.
    return JsonResponse({'success': False}) #Si el método no es POST, se retorna un JSON con el mensaje de error.

#Views para departamentos
@csrf_exempt # Decorador para deshabilitar la protección CSRF
def departamento_list(request): #Vista para listar los usuarios
    departamento = Departamentos.objects.all() #Se obtienen todos los usuarios de la base de datos.
    return render(request, 'SIGEA_APP/CRUD_DEPARTAMENTOS/departamento_list.html', {'departamento': departamento}) #Se renderiza la plantilla usuario_list.html con los usuarios obtenidos.

@csrf_exempt # Decorador para deshabilitar la protección CSRF
def departamento_create(request): #Vista para crear un usuario
    if request.method == 'POST': #Si el método es POST, se crea un formulario con los datos del usuario.
        form = DepartamentosForm(request.POST) #Se crea un formulario con los datos del usuario.
        if form.is_valid(): #Si el formulario es válido, se guarda el usuario en la base de datos.
            form.save() #Se guarda el usuario en la base de datos.
            return JsonResponse({'success': True}) #Se retorna un JSON con el mensaje de éxito.
        else:
            return JsonResponse({'success': False, 'errors': form.errors}) #Si el formulario no es válido, se retorna un JSON con el mensaje de error.
    else:
        form = DepartamentosForm()
    return render(request, 'SIGEA_APP/CRUD_DEPARTAMENTOS/departamento_form.html', {'form': form}) #Si el método no es POST, se muestra el formulario para crear un usuario.

@csrf_exempt # Decorador para deshabilitar la protección CSRF
def departamento_update(request, iddepartamento): # Usamos idusuario aquí #Vista para actualizar un usuario
    departamento = get_object_or_404(Departamentos, iddepartamento=iddepartamento) # y aquí también #Se obtiene el usuario a actualizar.
    if request.method == 'POST': #Si el método es POST, se crea un formulario con los datos del usuario.
        form = DepartamentosForm(request.POST, instance=departamento) #Se crea un formulario con los datos del usuario.
        if form.is_valid():#Si el formulario es válido, se actualiza el usuario en la base de datos.
            form.save() #Se actualiza el usuario en la base de datos.
            return JsonResponse({'success': True}) #Se retorna un JSON con el mensaje de éxito.
        else:
            return JsonResponse({'success': False, 'errors': form.errors}) #Si el formulario no es válido, se retorna un JSON con el mensaje de error.
    else:
        form = DepartamentosForm(instance=departamento) #Si el método no es POST, se muestra el formulario para actualizar un usuario.
    return render(request, 'SIGEA_APP/CRUD_DEPARTAMENTOS/departamento_form.html', {'form': form}) #Se renderiza la plantilla usuario_form.html con el formulario para actualizar un usuario.

def departameto_detail(request, iddepartamento):  # Usamos idusuario aquí #Vista para ver los detalles de un usuario
    departamento = get_object_or_404(Departamentos, iddepartamento=iddepartamento)  # y aquí también #Se obtiene el usuario a mostrar.
    return render(request, 'SIGEA_APP/CRUD_DEPARTAMENTOS/departamento_detail.html', {'departameto': departamento}) #Se renderiza la plantilla usuario_detail.html con los datos del usuario.

@csrf_exempt # Decorador para deshabilitar la protección CSRF
def departamento_delete(request, iddepartamento):  # Usamos idusuario aquí #Vista para eliminar un usuario
    departamento = get_object_or_404(Departamentos	, iddepartamento=iddepartamento)  # y aquí también #Se obtiene el usuario a eliminar.
    if request.method == 'POST': #Si el método es POST, se elimina el usuario de la base de datos.
        departamento.delete() #Se elimina el usuario de la base de datos.
        return JsonResponse({'success': True}) #Se retorna un JSON con el mensaje de éxito.
    return JsonResponse({'success': False}) #Si el método no es POST, se retorna un JSON con el mensaje de error.

#Views para servicios
@csrf_exempt # Decorador para deshabilitar la protección CSRF
def servicio_list(request): #Vista para listar los usuarios
    servicios = Servicios.objects.all() #Se obtienen todos los usuarios de la base de datos.
    return render(request, 'SIGEA_APP/CRUD_SERVICIO/servicio_list.html', {'servicio': servicios}) #Se renderiza la plantilla usuario_list.html con los usuarios obtenidos.

@csrf_exempt # Decorador para deshabilitar la protección CSRF
def servicio_create(request): #Vista para crear un usuario
    if request.method == 'POST': #Si el método es POST, se crea un formulario con los datos del usuario.
        form = ServiciosForm(request.POST) #Se crea un formulario con los datos del usuario.
        if form.is_valid(): #Si el formulario es válido, se guarda el usuario en la base de datos.
            form.save() #Se guarda el usuario en la base de datos.
            return JsonResponse({'success': True}) #Se retorna un JSON con el mensaje de éxito.
        else:
            return JsonResponse({'success': False, 'errors': form.errors}) #Si el formulario no es válido, se retorna un JSON con el mensaje de error.
    else:
        form = ServiciosForm()
    return render(request, 'SIGEA_APP/CRUD_SERVICIO/servicio_form.html', {'form': form}) #Si el método no es POST, se muestra el formulario para crear un usuario.

@csrf_exempt
def servicio_update(request, idservicio):
    servicio = get_object_or_404(Servicios, idservicio=idservicio)
    if request.method == 'POST':
        form = ServiciosForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ServiciosForm(instance=servicio)
    return render(request, 'SIGEA_APP/CRUD_SERVICIO/servicio_form.html', {'form': form})

def servicio_detail(request, idservicio):  # Usamos idusuario aquí #Vista para ver los detalles de un usuario
    servicios = get_object_or_404(Servicios, idservicio=idservicio)  # y aquí también #Se obtiene el usuario a mostrar.
    return render(request, 'SIGEA_APP/CRUD_SERVICIO/servicio_detail.html', {'servicios': servicios}) #Se renderiza la plantilla usuario_detail.html con los datos del usuario.

@csrf_exempt # Decorador para deshabilitar la protección CSRF
def servicio_delete(request, idservicio):  # Usamos idusuario aquí #Vista para eliminar un usuario
    servicios = get_object_or_404(Servicios	, idservicio=idservicio)  # y aquí también #Se obtiene el usuario a eliminar.
    if request.method == 'POST': #Si el método es POST, se elimina el usuario de la base de datos.
        servicios.delete() #Se elimina el usuario de la base de datos.
        return JsonResponse({'success': True}) #Se retorna un JSON con el mensaje de éxito.
    return JsonResponse({'success': False}) #Si el método no es POST, se retorna un JSON con el mensaje de error.

def actividades(request):
    actividades = Actividades.objects.all()
    return render(request, 'SIGEA_APP/CRUD_EVENT/event.html', {'actividades':actividades})

@csrf_exempt
def actividades_create(request):
    if request.method == 'POST':
        nombreactividad = request.POST.get('nombreactividad')
        tipoactividad = request.POST.get('tipoactividad')
        descripcionactividad = request.POST.get('descripcionactividad')
        fechaactividad = request.POST.get('fechaactividad')
        fechafin = request.POST.get('fechafin')
        
        usuario = get_object_or_404(Usuario, email=request.user.email)

        print(f'nombre de actividad: {nombreactividad}, tipo: {tipoactividad}, descripcion: {descripcionactividad}, fecha: {fechaactividad}')

        # Crea un nuevo evento en la base de datos
        nuevo_evento = Actividades(nombreactividad=nombreactividad, descripcionactividad=descripcionactividad, fechaactividad=fechaactividad, tipoactividad=tipoactividad, idusuario=usuario, fechafin=fechafin)
        nuevo_evento.save()
        # Devuelve una respuesta JSON indicando que la creación del evento fue exitosa
        return JsonResponse({'success': True, 'message':'Has creado un evento exitosamente'})
    else:
        # Si la solicitud no es de tipo POST, devuelve un error
        return JsonResponse({'success': False, 'message': 'La solicitud debe ser de tipo POST'})
    
def actividades_list(request):
    actividades = Actividades.objects.all()
    actividades_json = []
    for acti in actividades:
        actividades_json.append({
            'title': acti.nombreactividad,
            'start': acti.fechaactividad.isoformat(),
            'end': acti.fechafin.isoformat(),
            'description': acti.descripcionactividad.format(),
            'typeact': acti.tipoactividad,
            'idacti':acti.idactividad
        })
    print(actividades_json)
    return JsonResponse(actividades_json, safe=False)

@csrf_exempt # Decorador para deshabilitar la protección CSRF
def actividad_delete(request, idactividad):  # Usamos idusuario aquí #Vista para eliminar un usuario
    actividad = get_object_or_404(Actividades, idactividad=idactividad)  # y aquí también #Se obtiene el usuario a eliminar.
    if request.method == 'POST': #Si el método es POST, se elimina el usuario de la base de datos.
        actividad.delete() #Se elimina el usuario de la base de datos.
        return JsonResponse({'success': True}) #Se retorna un JSON con el mensaje de éxito.
    return JsonResponse({'success': False}) #Si el método no es POST, se retorna un JSON con el mensaje de error.

@csrf_exempt
def recordatorio_create(request):
    if request.method == 'POST':
        nombrerecordatorio = request.POST.get('nombrerecordatorio')
        fecharecordatorio = request.POST.get('fecharecordatorio')
        descripcionrecordatorio = request.POST.get('descripcionrecordatorio')
        idactividad = request.POST.get('idactividad')
        idacti = Actividades.objects.get(idactividad=idactividad)

        # Crea un nuevo evento en la base de datos
        nuevo_recordatorio = Recordatorio(
            nombrerecordatorio=nombrerecordatorio, 
            descripcionrecordatorio=descripcionrecordatorio, 
            fecharecordatorio=fecharecordatorio,
            idactividad=idacti,
        )
        nuevo_recordatorio.save()
        # Devuelve una respuesta JSON indicando que la creación del evento fue exitosa
        return JsonResponse({'success': True, 'message':'Has creado un recordatorio exitosamente'})
    else:
        # Si la solicitud no es de tipo POST, devuelve un error
        return JsonResponse({'success': False, 'message': 'La solicitud debe ser de tipo POST'})
    
    
