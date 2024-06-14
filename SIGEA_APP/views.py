from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import *
from django.utils import timezone
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings

@login_required
def index(request):
    user_type = request.user.tipousuario.idtipousuario
    context = {'pruebita': user_type}
    if user_type == 1:  # Redirige al administrador
        return render(request, 'SIGEA_APP/admin/index.html', context)
    elif user_type == 2:  # Redirige a la secretaria
        return render(request, 'SIGEA_APP/secretaria/index.html', context)
    elif user_type == 3:  # Redirige al jefe de departamento
        return render(request, 'SIGEA_APP/jefe_departamento/index.html', context)
    elif user_type == 4:  # Redirige al abogado
        return render(request, 'SIGEA_APP/abogado/index.html', context)
    else:
        return redirect('login')
    
    
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



#Perfil de usuario
@login_required
def edit_profile(request):
    user_type = request.user.tipousuario.idtipousuario
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = EditProfileForm(instance=request.user)
    
    context = {
        'pruebita': user_type,
        'form': form
    }
    
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/edit_profile.html', context)


@csrf_exempt # Decorador para deshabilitar la protección CSRF
def usuario_list(request):
    user_type = request.user.tipousuario.idtipousuario
    context = {
        'pruebita': user_type,
        'usuarios': Usuario.objects.all()
    }
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_list.html', context)


@csrf_exempt
def usuario_create(request):
    if request.method == 'POST':

        # #ALLAN ESTUVO AQUI, CORREO DE CONFIRMACIÖN DE CREACIÖN DE USUARIO
        # subject = "¡Excelente! Se ha creado un usuario"
        # message ="Ahora formas parte de nuestra empresa, LANS LAW GLOBAL está feliz de tenerte, tus credenciales son:\nCorreo: "+request.POST["email"]+"\nContraseña: "+request.POST["password"]
        # email_from=settings.EMAIL_HOST_USER
        # recipient_list=[request.POST["email"]]
        # send_mail(subject, message, email_from, recipient_list, fail_silently=False)

        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UsuarioForm()
        if 'departamento_id' in request.GET:
            departamento_id = request.GET['departamento_id']
            servicios = Servicios.objects.filter(iddepartamento=departamento_id)
            return JsonResponse({'servicios': list(servicios.values('idservicio', 'nombreservicio'))})
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_form.html', {'form': form})

@csrf_exempt
def usuario_update(request, idusuario):
    usuario = get_object_or_404(Usuario, idusuario=idusuario)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_form.html', {'form': form})

def usuario_detail(request, idusuario):
    usuario = get_object_or_404(Usuario, idusuario=idusuario)
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_detail.html', {'usuario': usuario})

@csrf_exempt
def usuario_delete(request, idusuario):
    usuario = get_object_or_404(Usuario, idusuario=idusuario)
    if request.method == 'POST':
        usuario.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

#Views para departamentos
@csrf_exempt # Decorador para deshabilitar la protección CSRF
def departamento_list(request): #Vista para listar los usuarios
    user_type = request.user.tipousuario.idtipousuario
    context = {
        'pruebita': user_type,
        'departamento': Departamentos.objects.all() #Se obtienen todos los usuarios de la base de datos.
    }
    
    return render(request, 'SIGEA_APP/CRUD_DEPARTAMENTOS/departamento_list.html', context) #Se renderiza la plantilla usuario_list.html con los usuarios obtenidos.

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
    user_type = request.user.tipousuario.idtipousuario
    context = {
        'pruebita': user_type,
        'servicio': Servicios.objects.all() #NOTA: La variable es "servicio" no "servicios"
    }
    return render(request, 'SIGEA_APP/CRUD_SERVICIO/servicio_list.html', context) #Se renderiza la plantilla usuario_list.html con los usuarios obtenidos.

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


#ACTIVIDADES
@login_required
def actividades(request):
    user_type = request.user.tipousuario.idtipousuario
    actividades = Actividades.objects.all()
    usuarios = Usuario.objects.all()
    
    context = {
        'pruebita': user_type,
        'actividades': actividades,
        'usuarios': usuarios
    }
    
    return render(request, 'SIGEA_APP/CRUD_EVENT/event.html', context)

@csrf_exempt
def actividades_create(request):
    if request.method == 'POST':

        nombreactividad = request.POST.get('nombreactividad')
        tipoactividad = request.POST.get('tipoactividad')
        descripcionactividad = request.POST.get('descripcionactividad')
        fechaactividad = request.POST.get('fechaactividad')
        fechafin = request.POST.get('fechafin')
        invitados_ids = request.POST.getlist('invitadosactividad')
        
        usuario = get_object_or_404(Usuario, email=request.user.email)


        print(f'nombre de actividad: {nombreactividad}, tipo: {tipoactividad}, descripcion: {descripcionactividad}, fecha: {fechaactividad}')
        
        # Crea un nuevo evento en la base de datos
        nuevo_evento = Actividades(nombreactividad=nombreactividad, descripcionactividad=descripcionactividad, fechaactividad=fechaactividad, tipoactividad=tipoactividad, idusuario=usuario, fechafin=fechafin)
        nuevo_evento.save()
        
        for invitado_id in invitados_ids:
                invitado = get_object_or_404(Usuario, idusuario=invitado_id)
                nuevo_evento.invitadosactividad.add(invitado)
                #ALLAN ESTUVO AQUI, CORREO DE CONFIRMACIÖN DE CREACIÖN DE USUARIO
                # subject = "Se te ha invitado a una Actividad"
                # message = "Se le informa que ha sido invitado a participar en la actividad "+request.POST['nombreactividad']+", la actividad se llevará acabo desde: \nInicio: "+request.POST['fechaactividad']+"\nFin: "+request.POST['fechafin']+"\n¡TE ESPERAMOS!"
                # email_from=settings.EMAIL_HOST_USER
                # recipient_list=[invitado.email]
                # send_mail(subject, message, email_from, recipient_list, fail_silently=False)

        # Devuelve una respuesta JSON indicando que la creación del evento fue exitosa
        return JsonResponse({'success': True, 'message':'Has creado un evento exitosamente'})
    else:
        # Si la solicitud no es de tipo POST, devuelve un error
        return JsonResponse({'success': False, 'message': 'La solicitud debe ser de tipo POST'})

def search_users(request):
    query = request.GET.get('q')
    usuarios = Usuario.objects.filter(nombre__icontains=query) | Usuario.objects.filter(apellido__icontains=query)
    results = [{'id': usuario.idusuario, 'nombre': usuario.nombre, 'apellido': usuario.apellido} for usuario in usuarios]
    return JsonResponse(results, safe=False)


def actividades_list(request):
    actividades = Actividades.objects.all()
    actividades_json = []
    
    for acti in actividades:
        invitados = acti.invitadosactividad.all()  # Obtener todos los invitados de la actividad
        invitados_list = []
        for invitado in invitados:
            invitados_list.append({
                'nombre': invitado.nombre,
                'apellido': invitado.apellido,
            })
        
        actividades_json.append({
            'title': acti.nombreactividad,
            'start': acti.fechaactividad.isoformat(),
            'end': acti.fechafin.isoformat(),
            'description': acti.descripcionactividad.format(),
            'typeact': acti.tipoactividad,
            'idacti': acti.idactividad,
            'invitados': invitados_list,
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

