from django import forms
from django.contrib.auth.hashers import make_password #Se importa la función make_password para encriptar la contraseña.
from .models import *

# forms.py

class UsuarioForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(
        queryset=Departamentos.objects.all(),
        empty_label="Selecciona un Departamento",
        required=True,
        label='Departamento'
    )

    class Meta:
        model = Usuario
        fields = [
            'departamento', 'idservicio', 'nombre', 'apellido', 'dui', 'telefono', 'salario', 'email', 'password', 'tipousuario', 'foto_perfil'
        ]
        labels = {
            'departamento': 'Departamento: ',
            'idservicio': 'Servicio: ',
            'nombre': 'Nombre: ',
            'apellido': 'Apellido: ',
            'dui': 'DUI: ',
            'telefono': 'Teléfono: ',
            'salario': 'Salario: ',
            'email': 'Email: ',
            'password': 'Contraseña: ',
            'tipousuario': 'Tipo de Usuario: ',
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
