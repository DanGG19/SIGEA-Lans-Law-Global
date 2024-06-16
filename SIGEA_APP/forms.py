from django import forms 
from django.contrib.auth.hashers import make_password #Se importa la función make_password para encriptar la contraseña.
from .models import * #Se importan todos los modelos de la aplicación.

# forms.py

class UsuarioForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(
        queryset=Departamentos.objects.all(),
        empty_label="Selecciona un Departamento",
        required=True,
        label='Departamento',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    divisiondepartamento = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    tipousuario = forms.ModelChoiceField(
        queryset=TipoUsuario.objects.all(),
        empty_label="Seleccione el tipo de usuario",
        required=True,
        label='Tipo de Usuario',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = [
            'departamento', 'idservicio', 'nombre', 'apellido', 'dui', 'telefono', 'salario', 'email', 'password', 'tipousuario', 'foto_perfil', 'divisiondepartamento'
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
            'foto_perfil': 'Foto de Perfil: ',
            'divisiondepartamento': ''
        }
        widgets = {
            'idservicio': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dui': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'tipousuario': forms.Select(attrs={'class': 'form-control'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
            'divisiondepartamento': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.idservicio:
            self.fields['departamento'].initial = self.instance.idservicio.iddepartamento

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if self.cleaned_data['password']:
            usuario.password = make_password(self.cleaned_data['password'])
        if commit:
            usuario.save()
        return usuario





class DepartamentosForm(forms.ModelForm):
    responsabledepartamento = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        empty_label="Seleccione un responsable",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Responsable de Departamento"
    )

    class Meta:
        model = Departamentos
        fields = ['divisiondepartamento', 'responsabledepartamento']
        labels = {
            'divisiondepartamento': 'División de Departamento: ',
            'responsabledepartamento': 'Responsable de Departamento'
        }
        widgets = {
            'divisiondepartamento': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.responsabledepartamento:
            self.fields['responsabledepartamento'].initial = Usuario.objects.get(email=self.instance.responsabledepartamento)
        self.fields['responsabledepartamento'].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellido}"
        

class ServiciosForm(forms.ModelForm):
    iddepartamento = forms.ModelChoiceField(
        queryset=Departamentos.objects.all(),
        empty_label="Seleccione departamento",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Departamento'
    )

    class Meta:
        model = Servicios
        fields = ['iddepartamento', 'nombreservicio', 'descripcionservicio']
        labels = {
            'iddepartamento': 'Departamento',
            'nombreservicio': 'Nombre del servicio',
            'descripcionservicio': 'Descripcion del servicio'
        }
        widgets = {
            'iddepartamento': forms.Select(attrs={'class': 'form-control'}),
            'nombreservicio': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcionservicio': forms.Textarea(attrs={'class': 'form-control'}),
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'dui', 'telefono', 'email', 'foto_perfil']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dui': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
        }
        

class UsuarioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    
    
class ActividadesForm(forms.ModelForm):
    class Meta:
        model = Actividades
        fields = ['idactividad', 'nombreactividad', 'fechaactividad', 'fechafin', 'tipoactividad', 'descripcionactividad', 'invitadosactividad', 'docanexoactividad']
        labels = {
            'nombreactividad': 'Nombre de la actividad',
            'fechaactividad':'Fecha de inicio',
            'fechafin': 'Fecha de finalizacion', 
            'tipoactividad': 'Tipo de actividad', 
            'descripcionactividad': 'descripcion de la actividad', 
            'invitadosactividad': 'invitados a la actividad', 
            'docanexoactividad':'Documentos agregados'
        }
        widgets = {
            'idactividad': forms.HiddenInput(),
            'nombreactividad': forms.TextInput(attrs={'class': 'form-control',
                                                      'disabled': False}),
            'fechaactividad': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'  
            ),
              'fechafin': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'  
            ),
            'tipoactividad': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcionactividad': forms.Textarea(attrs={'class': 'form-control'}),
            
        }

class EvaluacionForm(forms.ModelForm):
    idusuario = UsuarioChoiceField(
        queryset=Usuario.objects.all(),
        empty_label="Seleccione usuario",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Usuario'
    )

    class Meta:
        model = Evaluacion
        fields = ['idusuario', 'tipoevaluacion', 'notaevaluacio', 'comentarioevaluacio', 'fechaevaluacion']
        labels = {
            'idusuario': 'Usuario: ',
            'tipoevaluacion': 'Tipo de Evaluación: ',
            'notaevaluacio': 'Nota de Evaluación: ',
            'comentarioevaluacio': 'Comentario: ',
            'fechaevaluacion': 'Fecha de Evaluación: '
        }
        widgets = {
            'idusuario': forms.Select(attrs={'class': 'form-control'}),
            'tipoevaluacion': forms.TextInput(attrs={'class': 'form-control'}),
            'notaevaluacio': forms.NumberInput(attrs={'class': 'form-control',
                                                      'min': 1,
                                                      'max': 10}),
            'comentarioevaluacio': forms.Textarea(attrs={'class': 'form-control'}),
            'fechaevaluacion': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'  # Ajusta el formato según tu necesidad
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EvaluacionForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['fechaevaluacion'].initial = self.instance.fechaevaluacion.strftime('%Y-%m-%dT%H:%M')

class PlanDesarolloForm(forms.ModelForm):
    class Meta:
        model = Plandesarrollo
        fields = ['idevaluacion', 'nombreplandes', 'objetivosplandes', 'alcancesplandes', 
        'descripcionplandes', 'instruccionesplandes', 'duracionmesesplandes',
        'fortalezas', 'debilidades', 'oportunidades', 'amenazas']   
        widgets = {
            'idevaluacion': forms.HiddenInput(),
            'nombreplandes': forms.TextInput(attrs={'class': 'form-control'}),
            'objetivosplandes': forms.Textarea(attrs={'class': 'form-control',
                                                      'rows': 7,
                                                      'style': 'resize: none'}),
            'alcancesplandes': forms.Textarea(attrs={'class': 'form-control',
                                                      'rows': 7,
                                                      'style': 'resize: none'}),
            'descripcionplandes': forms.Textarea(attrs={'class': 'form-control',
                                                      'rows': 7,
                                                      'style': 'resize: none'}),
            'instruccionesplandes': forms.Textarea(attrs={'class': 'form-control',
                                                      'rows': 7,
                                                      'style': 'resize: none'}),
            'duracionmesesplandes': forms.NumberInput(attrs={'class': 'form-control',
                                                             'min': 1}),
            'fortalezas': forms.Textarea(attrs={'class': 'form-control',
                                                 'style': 'resize: none'}),
            'debilidades': forms.Textarea(attrs={'class': 'form-control',
            'style': 'resize: none'}),
            'oportunidades': forms.Textarea(attrs={'class': 'form-control',
            'style': 'resize: none'}),
            'amenazas': forms.Textarea(attrs={'class': 'form-control',
            'style': 'resize: none'}),
        }
            
