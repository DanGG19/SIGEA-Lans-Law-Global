from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import *
from django.utils import timezone
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings


def admin_or_secretaria_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        user_type = request.user.tipousuario.idtipousuario
        if user_type == 1 or user_type == 2:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('404')
    return _wrapped_view_func


def admin_or_secretaria_or_jefe_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        user_type = request.user.tipousuario.idtipousuario
        if user_type == 1 or user_type == 2 or user_type == 3:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('404')
    return _wrapped_view_func



@login_required
def vista404(request):
    return render(request, 'SIGEA_APP/404.html')

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

def exit(request):
    logout(request)
    return redirect('login')

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

@login_required
@csrf_exempt # Decorador para deshabilitar la protección CSRF
@admin_or_secretaria_required
def usuario_list(request):
    user_type = request.user.tipousuario.idtipousuario
    context = {
        'pruebita': user_type,
        'usuarios': Usuario.objects.all()
    }
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_list.html', context)

@login_required
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
            departamento_id = request.GET.get('departamento_id')
            if departamento_id:
                servicios = Servicios.objects.filter(iddepartamento=departamento_id)
                departamento = Departamentos.objects.get(pk=departamento_id)
                return JsonResponse({
                    'servicios': list(servicios.values('idservicio', 'nombreservicio')),
                    'division': departamento.divisiondepartamento
                })
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_form.html', {'form': form})

@login_required
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
        initial_data = {
            'divisiondepartamento': usuario.idservicio.iddepartamento.divisiondepartamento if usuario.idservicio else ''
        }
        form.initial.update(initial_data)
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_form.html', {'form': form})

@login_required
def usuario_detail(request, idusuario):
    usuario = get_object_or_404(Usuario, idusuario=idusuario)
    return render(request, 'SIGEA_APP/CRUD_USUARIOS/usuario_detail.html', {'usuario': usuario})

@login_required
@csrf_exempt
def usuario_delete(request, idusuario):
    usuario = get_object_or_404(Usuario, idusuario=idusuario)
    if request.method == 'POST':
        usuario.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

#Views para departamentos
@login_required
@admin_or_secretaria_or_jefe_required
def departamento_list(request): 
    user_type = request.user.tipousuario.idtipousuario
    departamentos = Departamentos.objects.all()
    departamentos_con_responsables = []

    for depto in departamentos:
        try:
            responsable = Usuario.objects.get(email=depto.responsabledepartamento)
            departamentos_con_responsables.append({
                'iddepartamento': depto.iddepartamento,
                'divisiondepartamento': depto.divisiondepartamento,
                'responsable_nombre': responsable.nombre,
                'responsable_apellido': responsable.apellido,
                'responsable_email': responsable.email
            })
        except Usuario.DoesNotExist:
            departamentos_con_responsables.append({
                'iddepartamento': depto.iddepartamento,
                'divisiondepartamento': depto.divisiondepartamento,
                'responsable_nombre': None,
                'responsable_apellido': None,
                'responsable_email': depto.responsabledepartamento
            })

    context = {
        'pruebita': user_type,
        'departamentos': departamentos_con_responsables
    }
    
    return render(request, 'SIGEA_APP/CRUD_DEPARTAMENTOS/departamento_list.html', context)

@login_required
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

@login_required
@csrf_exempt # Decorador para deshabilitar la protección CSRF
def departamento_update(request, iddepartamento):
    departamento = get_object_or_404(Departamentos, iddepartamento=iddepartamento)
    if request.method == 'POST':
        form = DepartamentosForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = DepartamentosForm(instance=departamento)
        initial_data = {
            'responsabledepartamento': departamento.responsabledepartamento
        }
        form.initial.update(initial_data)
    return render(request, 'SIGEA_APP/CRUD_DEPARTAMENTOS/departamento_form.html', {'form': form})

def departameto_detail(request, iddepartamento):  # Usamos idusuario aquí #Vista para ver los detalles de un usuario
    departamento = get_object_or_404(Departamentos, iddepartamento=iddepartamento)  # y aquí también #Se obtiene el usuario a mostrar.
    return render(request, 'SIGEA_APP/CRUD_DEPARTAMENTOS/departamento_detail.html', {'departameto': departamento}) #Se renderiza la plantilla usuario_detail.html con los datos del usuario.


@login_required
@csrf_exempt # Decorador para deshabilitar la protección CSRF
def departamento_delete(request, iddepartamento):  # Usamos idusuario aquí #Vista para eliminar un usuario
    departamento = get_object_or_404(Departamentos	, iddepartamento=iddepartamento)  # y aquí también #Se obtiene el usuario a eliminar.
    if request.method == 'POST': #Si el método es POST, se elimina el usuario de la base de datos.
        departamento.delete() #Se elimina el usuario de la base de datos.
        return JsonResponse({'success': True}) #Se retorna un JSON con el mensaje de éxito.
    return JsonResponse({'success': False}) #Si el método no es POST, se retorna un JSON con el mensaje de error.

#Views para servicios
@login_required
@admin_or_secretaria_required
@csrf_exempt # Decorador para deshabilitar la protección CSRF
def servicio_list(request): #Vista para listar los usuarios
    user_type = request.user.tipousuario.idtipousuario
    context = {
        'pruebita': user_type,
        'servicio': Servicios.objects.all() #NOTA: La variable es "servicio" no "servicios"
    }
    return render(request, 'SIGEA_APP/CRUD_SERVICIO/servicio_list.html', context) #Se renderiza la plantilla usuario_list.html con los usuarios obtenidos.

@login_required
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

@login_required
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

@login_required
def servicio_detail(request, idservicio):  # Usamos idusuario aquí #Vista para ver los detalles de un usuario
    servicios = get_object_or_404(Servicios, idservicio=idservicio)  # y aquí también #Se obtiene el usuario a mostrar.
    return render(request, 'SIGEA_APP/CRUD_SERVICIO/servicio_detail.html', {'servicios': servicios}) #Se renderiza la plantilla usuario_detail.html con los datos del usuario.

@login_required
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

@login_required
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

@login_required
def search_users(request):
    query = request.GET.get('q')
    usuarios = Usuario.objects.filter(nombre__icontains=query) | Usuario.objects.filter(apellido__icontains=query)
    results = [{'id': usuario.idusuario, 'nombre': usuario.nombre, 'apellido': usuario.apellido} for usuario in usuarios]
    return JsonResponse(results, safe=False)

@login_required
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

@login_required
@csrf_exempt # Decorador para deshabilitar la protección CSRF
def actividad_delete(request, idactividad):  # Usamos idusuario aquí #Vista para eliminar un usuario
    actividad = get_object_or_404(Actividades, idactividad=idactividad)  # y aquí también #Se obtiene el usuario a eliminar.
    if request.method == 'POST': #Si el método es POST, se elimina el usuario de la base de datos.
        actividad.delete() #Se elimina el usuario de la base de datos.
        return JsonResponse({'success': True}) #Se retorna un JSON con el mensaje de éxito.
    return JsonResponse({'success': False}) #Si el método no es POST, se retorna un JSON con el mensaje de error.

@login_required
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

@login_required
@admin_or_secretaria_or_jefe_required
@csrf_exempt
def evaluacion_list(request):
    user_type = request.user.tipousuario.idtipousuario
    
    context = {
        'pruebita': user_type,
        'evaluaciones': Evaluacion.objects.all(),
        'plandes': Plandesarrollo.objects.all()
        }
    return render(request, 'SIGEA_APP/CRUD_EVALUACIONES/evaluacion_list.html', context)

@login_required
@csrf_exempt
def evaluacion_create(request):
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EvaluacionForm()
    return render(request, 'SIGEA_APP/CRUD_EVALUACIONES/evaluacion_form.html', {'form': form})

@login_required
@csrf_exempt
def evaluacion_update(request, idevaluacion):
    evaluacion = get_object_or_404(Evaluacion, idevaluacion=idevaluacion)
    if request.method == 'POST':
        form = EvaluacionForm(request.POST, instance=evaluacion)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EvaluacionForm(instance=evaluacion)
    return render(request, 'SIGEA_APP/CRUD_EVALUACIONES/evaluacion_form.html', {'form': form})

@login_required
def evaluacion_detail(request, idevaluacion):
    evaluacion = get_object_or_404(Evaluacion, idevaluacion=idevaluacion)
    return render(request, 'SIGEA_APP/CRUD_EVALUACIONES/evaluacion_detail.html', {'evaluacion': evaluacion})

@login_required
@csrf_exempt
def evaluacion_delete(request, idevaluacion):
    evaluacion = get_object_or_404(Evaluacion, idevaluacion=idevaluacion)
    if request.method == 'POST':
        evaluacion.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
@csrf_exempt
@admin_or_secretaria_or_jefe_required
def plandesarrollo_create(request, idevaluacion):
    if request.method == 'POST':
        eva = Evaluacion.objects.get(idevaluacion=idevaluacion)
        data = request.POST.copy()
        data['idevaluacion'] = eva
        DF = PlanDesarolloForm(data)
        if DF.is_valid():
            d = DF.save()
            eva.idplandes = d
            eva.save()
            
            return redirect('evaluacion_list')
        else:
            return redirect('evaluacion_list')

    else:
        DesarolloForm = PlanDesarolloForm()
        user_type = request.user.tipousuario.idtipousuario
        context = {
            'pruebita': user_type,
            'DesarolloForm': DesarolloForm
        }
    return render(request, 'SIGEA_APP/PLANESDES/plandesarrollo_create.html', context)