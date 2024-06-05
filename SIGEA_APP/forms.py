from django import forms
from django.contrib.auth.hashers import make_password #Se importa la función make_password para encriptar la contraseña.
from .models import *

class UsuarioForm(forms.ModelForm): #Se crea un formulario para el modelo Usuario.
    class Meta: #Se define la clase Meta.
        model = Usuario #Define el modelo Usuario para el formulario. 
        fields = [ #Se definen los campos del formulario.
            'nombre', 'apellido', 'dui', 'telefono', 'salario', 'email', 'password', 'tipousuario', 'idservicio'  #Lista de campos del modelo que estarán en el formulario.
        ]
        labels = { #Se definen las etiquetas de los campos del formulario.
            'nombre':'Nombre: ', #Etiqueta para el campo nombre.
            'apellido':'Apellido: ', #Etiqueta para el campo apellido.
            'dui':'DUI: ', #Etiqueta para el campo dui.
            'telefono':'Teléfono: ', #Etiqueta para el campo teléfono.
            'salario':'Salario: ', #Etiqueta para el campo salario.
            'email':'Email: ', #Etiqueta para el campo email.
            'password':'Contraseña: ', #Etiqueta para el campo password.
            'tipousuario':'Tipo de Usuario: ', #Etiqueta para el campo tipousuario.
            'idservicio':'Servicio: ' #Etiqueta para el campo idservicio.
        }
        
        
        widgets = {
            'password': forms.PasswordInput(),#Configura el widget PasswordInput para el campo password para que se oculte el texto ingresado.
        }
        
    def save(self, commit=True): #Se sobrescribe el método save para encriptar la contraseña antes de guardar el usuario.
        usuario = super().save(commit=False) #Se llama al método save de la clase padre.
        if self.cleaned_data['password']: #Si el campo password no está vacío, se encripta la contraseña.
            usuario.password = make_password(self.cleaned_data['password']) #Se encripta la contraseña.
        if commit: #Si commit es True, se guarda el usuario en la base de datos.
            usuario.save() #Se guarda el usuario en la base de datos.
        return usuario #Se retorna el usuario guardado.
        
class DepartamentosForm(forms.ModelForm):
    class Meta:
        model = Departamentos
        fields = ['divisiondepartamento', 'responsabledepartamento']
        labels = {'divisiondepartamento':'División de Departamento: ', 
                  'responsabledepartamento':'Responsable de Departamento'}
        

class ServiciosForm(forms.ModelForm):
    iddepartamento = forms.ModelChoiceField(
        queryset=Departamentos.objects.all(),
        label='Departamento',
        to_field_name='divisiondepartamento'
    )

    class Meta:
        model = Servicios
        fields = ['iddepartamento', 'nombreservicio', 'descripcionservicio']
        labels = {
            'iddepartamento': 'Departamento',
            'nombreservicio': 'Nombre del servicio',
            'descripcionservicio': 'Descripcion del servicio'
        }