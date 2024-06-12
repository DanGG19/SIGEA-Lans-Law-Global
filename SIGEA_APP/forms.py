from django import forms
from django.contrib.auth.hashers import make_password #Se importa la función make_password para encriptar la contraseña.
from .models import *

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre', 'apellido', 'dui', 'telefono', 'salario', 'email', 'password', 'tipousuario', 'idservicio', 'foto_perfil'
        ]
        labels = {
            'nombre': 'Nombre: ',
            'apellido': 'Apellido: ',
            'dui': 'DUI: ',
            'telefono': 'Teléfono: ',
            'salario': 'Salario: ',
            'email': 'Email: ',
            'password': 'Contraseña: ',
            'tipousuario': 'Tipo de Usuario: ',
            'idservicio': 'Servicio: ',
            'foto_perfil': 'Foto de Perfil: '
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if self.cleaned_data['password']:
            usuario.password = make_password(self.cleaned_data['password'])
        if commit:
            usuario.save()
        return usuario
    
        
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