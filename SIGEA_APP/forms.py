from django import forms
from django.contrib.auth.hashers import make_password #Se importa la función make_password para encriptar la contraseña.
from .models import Usuario

class UsuarioForm(forms.ModelForm): #Se crea un formulario para el modelo Usuario.
    class Meta: #Se define la clase Meta.
        model = Usuario #Define el modelo Usuario para el formulario. 
        fields = [ #Se definen los campos del formulario.
            'nombre', 'apellido', 'dui', 'telefono', 'salario', 'email', 'password', 'tipousuario', 'idservicio'  #Lista de campos del modelo que estarán en el formulario.
        ]
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
        

