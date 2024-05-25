from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #Se importa el decorador login_required para proteger las vistas
from django.contrib.auth import authenticate, login #Se importa authenticate y login para manejar la autenticación de los usuarios

@login_required #Se protege la vista para que solo los usuarios autenticados puedan acceder
def index(request):
    return render(request, 'SIGEA_APP/index.html') #Se renderiza la página index.html que se encuentra en la carpeta SIGEA_APP

def login_V(request): #Se crea la vista login_V para manejar el login de los usuarios en la aplicación
    if request.method == 'POST': #Si el método de la petición es POST se procede a autenticar al usuario con los datos ingresados en el formulario de login 
        email = request.POST['email'] #Se obtiene el email ingresado en el formulario 
        password = request.POST['password'] #Se obtiene la contraseña ingresada en el formulario
        user = authenticate(request, username=email, password=password) #Se autentica al usuario con el email y la contraseña ingresados
        if user is not None: #Si el usuario es autenticado correctamente se redirige a la página principal de la aplicación
            login(request, user) #Se inicia sesión con el usuario autenticado
            return redirect('index') #Se redirige a la página principal de la aplicación
        else:
            return render(request, 'registration/login.html', {'error_message':'Datos Incorrectos'}) #Si los datos son incorrectos se renderiza la página de login con un mensaje de error
    return render(request, 'registration/login.html') #Si el método de la petición no es POST se renderiza la página de login
