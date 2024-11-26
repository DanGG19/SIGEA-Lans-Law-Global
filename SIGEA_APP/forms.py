from django import forms 
from django.contrib.auth.hashers import make_password #Se importa la función make_password para encriptar la contraseña.
from .models import * #Se importan todos los modelos de la aplicación.
from django.core.exceptions import ValidationError

# forms.py

class UsuarioForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(
        queryset=Departamentos.objects.all(),
        empty_label="Selecciona un Departamento",
        required=False,
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
    eliminar_foto = forms.BooleanField(
        required=False,
        label="Eliminar foto de perfil actual",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Usuario
        fields = [
            'departamento', 'idservicio', 'nombre', 'apellido', 'dui', 'telefono', 
            'salario', 'email', 'password', 'tipousuario', 'foto_perfil', 'divisiondepartamento'
        ]
        labels = {
            'departamento': 'Departamento',
            'idservicio': 'Servicio',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'dui': 'DUI',
            'telefono': 'Teléfono',
            'salario': 'Salario',
            'email': 'Email',
            'password': 'Contraseña',
            'tipousuario': 'Tipo de Usuario',
            'foto_perfil': 'Foto de Perfil',
            'divisiondepartamento': ''
        }
        widgets = {
            'idservicio': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dui': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9', 'pattern': '\\d{8}-\\d', 'title': 'El DUI debe tener el formato 12345678-9'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234-5678', 'pattern': '\\d{4}-\\d{4}', 'title': 'El teléfono debe tener el formato 1234-5678'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'tipousuario': forms.Select(attrs={'class': 'form-control'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
            'divisiondepartamento': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Si se está editando un usuario existente, hacer que el campo de contraseña no sea obligatorio
            self.fields['password'].required = False
            self.fields['password'].widget.attrs['placeholder'] = 'Deja en blanco para mantener la contraseña actual'
        if self.instance and self.instance.idservicio:
            self.fields['departamento'].initial = self.instance.idservicio.iddepartamento

    def save(self, commit=True):
        usuario = super().save(commit=False)
        
        # Eliminar la foto actual si se selecciona "Eliminar foto" y no es la predeterminada
        if self.cleaned_data.get('eliminar_foto') and usuario.foto_perfil and usuario.foto_perfil.name != 'fotos_perfil/perfil-del-usuario.png':
            usuario.foto_perfil.delete(save=False)  # Elimina la imagen actual del almacenamiento
            usuario.foto_perfil = 'fotos_perfil/perfil-del-usuario.png'  # Asigna la imagen por defecto

        # Actualiza la contraseña solo si se proporciona una nueva
        if self.cleaned_data['password']:
            usuario.password = make_password(self.cleaned_data['password'])
        else:
            usuario.password = Usuario.objects.get(pk=self.instance.pk).password

        if commit:
            usuario.save()
        return usuario



class DepartamentosForm(forms.ModelForm):
    responsabledepartamento = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        empty_label="Seleccione un responsable",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Responsable de Departamento",
        required=False
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
    eliminar_foto = forms.BooleanField(
        required=False,
        label="Eliminar foto de perfil actual",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'dui', 'telefono', 'email', 'foto_perfil']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dui': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9', 'pattern': '\\d{8}-\\d', 'title': 'El DUI debe tener el formato 12345678-9'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234-5678', 'pattern': '\\d{4}-\\d{4}', 'title': 'El teléfono debe tener el formato 1234-5678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        
        # Eliminar la foto si se selecciona "Eliminar foto" y no es la predeterminada
        if self.cleaned_data.get('eliminar_foto') and usuario.foto_perfil and usuario.foto_perfil.name != 'fotos_perfil/perfil-del-usuario.png':
            usuario.foto_perfil.delete(save=False)
            usuario.foto_perfil = 'fotos_perfil/perfil-del-usuario.png'
        
        if commit:
            usuario.save()
        return usuario

        

class UsuarioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    
    
class ActividadesForm(forms.ModelForm):

    invitadosactividad = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,

    )
    class Meta:
        model = Actividades
        fields = ['idactividad', 'nombreactividad', 'fechaactividad', 'fechafin', 'tipoactividad', 'descripcionactividad', 'docanexoactividad']
        labels = {
            'nombreactividad': 'Nombre de la actividad',
            'fechaactividad':'Fecha de inicio',
            'fechafin': 'Fecha de finalizacion', 
            'tipoactividad': 'Tipo de actividad', 
            'descripcionactividad': 'descripcion de la actividad', 
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
            'tipoactividad': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcionactividad': forms.Textarea(attrs={'class': 'form-control'}),
            'docanexoactividad': forms.FileInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        all_usuarios = Usuario.objects.all()
        self.fields['invitadosactividad'].queryset = all_usuarios
        self.fields['invitadosactividad'].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellido}"

        if self.instance:
            invitados = invitados_actividad.objects.filter(idactividad=self.instance).values_list('idusuario', flat=True)
            self.initial['invitadosactividad'] = invitados

    def save(self, commit=True):
        actividad = super().save(commit=False)
        if commit:
            actividad.save()
            self.save_m2m()  # Guardar relaciones many-to-many, como los invitados


class EvaluacionForm(forms.ModelForm):
    TIPO_EVALUACION_CHOICES = [
        ('Evaluación de Desempeño', 'Evaluación de Desempeño'),
        ('Evaluación Técnica', 'Evaluación Técnica'),
        ('Evaluación de Habilidades Blandas', 'Evaluación de Habilidades Blandas'),
        ('Evaluación de Cumplimiento', 'Evaluación de Cumplimiento'),
        ('Evaluación de Productividad', 'Evaluación de Productividad'),
        ('Evaluación de Conocimientos', 'Evaluación de Conocimientos'),
    ]

    tipoevaluacion = forms.ChoiceField(
        choices=TIPO_EVALUACION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo de Evaluación'
    )
    
    idusuario = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        empty_label="Seleccione usuario",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Empleado',
        required=True
    )

    class Meta:
        model = Evaluacion
        fields = ['idusuario', 'tipoevaluacion', 'notaevaluacio', 'comentarioevaluacio', 'fechaevaluacion']
        labels = {
            'notaevaluacio': 'Nota de Evaluación:',
            'comentarioevaluacio': 'Comentario:',
            'fechaevaluacion': 'Fecha de Evaluación:'
        }
        widgets = {
            'notaevaluacio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'comentarioevaluacio': forms.Textarea(attrs={'class': 'form-control'}),
            'fechaevaluacion': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def clean_notaevaluacio(self):
        nota = self.cleaned_data.get('notaevaluacio')
        if nota < 0 or nota > 100:
            raise forms.ValidationError("La nota debe estar entre 0 y 100.")
        return nota

    def __init__(self, *args, **kwargs):
        jefe_departamento = kwargs.pop('jefe_departamento', None)
        super(EvaluacionForm, self).__init__(*args, **kwargs)

        # Filtra usuarios según el jefe de departamento, si es necesario
        if jefe_departamento:
            self.fields['idusuario'].queryset = Usuario.objects.filter(idservicio__iddepartamento=jefe_departamento)
        
        # Predefine la fecha de evaluación
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['idevaluacion'].initial = self.instance.idevaluacion


class TipoClienteChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.descripcion}"

class ClienteForm(forms.ModelForm):
    idTipo = TipoClienteChoiceField(
        queryset=TipoCliente.objects.all(),
        empty_label="Seleccione el tipo de cliente:",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo del Cliente'
    )

    class Meta:
        model = Cliente
        fields = ['idTipo', 'nombre', 'correo', 'telefono']
        labels = {
            'idTipo': 'Tipo de Cliente: ',
            'nombre': 'Nombre del Cliente: ',
            'correo': 'Correo: ',
            'telefono': 'Teléfono: ',
        }
        widgets = {
            'idTipo': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'})
        }

class CasoForm(forms.ModelForm):
    idCliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        empty_label="Seleccione un cliente",
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Dueño del caso",
        required=True
    )

    class Meta:
        model = Caso
        fields = ['nombreCaso', 'idCliente', 'descripcionCaso', 'estadoCaso']
        labels = {
            'nombreCaso': 'Nombre del Caso: ',
            'idCliente': 'Cliente: ',
            'descripcionCaso': 'Descripción del Caso: ',
            'estadoCaso': 'Estado del Caso: '
        }
        widgets = {
            'nombreCaso': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcionCaso': forms.Textarea(attrs={'class': 'form-control'}),
            'estadoCaso': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idCliente'].label_from_instance = lambda obj: f"{obj.nombre}"
        
        
class RegistroAsistenciaForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(
        queryset=Usuario.objects.all(),
        empty_label="Seleccione un empleado",  
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = RegistroAsistencia
        fields = ['empleado', 'fecha', 'hora_entrada', 'hora_salida']
        labels = {
            'empleado': 'Empleado',
            'fecha': 'Fecha',
            'hora_entrada': 'Hora de Entrada',
            'hora_salida': 'Hora de Salida'
        }
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'},
                format='%Y-%m-%d' 
            ),
            'hora_entrada': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_salida': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].input_formats = ['%Y-%m-%d']
        self.fields['empleado'].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellido}"  