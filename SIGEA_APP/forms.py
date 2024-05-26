from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre', 'apellido', 'dui', 'telefono', 'salario', 'email', 'password', 'tipousuario', 'idservicio'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }
        

