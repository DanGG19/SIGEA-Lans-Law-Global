from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser # Se importan las clases BaseUserManager y AbstractBaseUser de django para manejar la creación de usuarios

# Create your models here.

class Actividades(models.Model):
    idactividad = models.AutoField(db_column='IDACTIVIDAD', primary_key=True)  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='IDUSUARIO')  # Field name made lowercase.
    idrecordatorio = models.ForeignKey('Recordatorio', models.DO_NOTHING, db_column='IDRECORDATORIO', blank=True, null=True)  # Field name made lowercase.
    tipoactividad = models.CharField(db_column='TIPOACTIVIDAD', max_length=255)  # Field name made lowercase.
    nombreactividad = models.CharField(db_column='NOMBREACTIVIDAD', max_length=255)  # Field name made lowercase.
    fechaactividad = models.DateTimeField(db_column='FECHAACTIVIDAD')  # Field name made lowercase.
    fechafin = models.DateTimeField(db_column='FECHAFIN')  # Field name made lowercase.
    descripcionactividad = models.CharField(db_column='DESCRIPCIONACTIVIDAD', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    invitadosactividad = models.CharField(db_column='INVITADOSACTIVIDAD', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    docanexoactividad = models.CharField(db_column='DOCANEXOACTIVIDAD', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'actividades'


class Departamentos(models.Model):
    iddepartamento = models.AutoField(db_column='IDDEPARTAMENTO', primary_key=True)  # Field name made lowercase.
    divisiondepartamento = models.CharField(db_column='DIVISIONDEPARTAMENTO', max_length=255)  # Field name made lowercase.
    responsabledepartamento = models.CharField(db_column='RESPONSABLEDEPARTAMENTO', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'departamentos'
        
    def __str__(self):
        return self.divisiondepartamento


class Evaluacion(models.Model):
    idevaluacion = models.AutoField(db_column='IDEVALUACION', primary_key=True)  # Field name made lowercase.
    idplandes = models.ForeignKey('Plandesarrollo', models.DO_NOTHING, db_column='IDPLANDES', blank=True, null=True)  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='IDUSUARIO')  # Field name made lowercase.
    tipoevaluacion = models.CharField(db_column='TIPOEVALUACION', max_length=255)  # Field name made lowercase.
    notaevaluacio = models.DecimalField(db_column='NOTAEVALUACIO', max_digits=10, decimal_places=0)  # Field name made lowercase.
    comentarioevaluacio = models.CharField(db_column='COMENTARIOEVALUACIO', max_length=2000)  # Field name made lowercase.
    fechaevaluacion = models.DateTimeField(db_column='FECHAEVALUACION')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'evaluacion'


class Plandesarrollo(models.Model):
    idplandes = models.AutoField(db_column='IDPLANDES', primary_key=True)  # Field name made lowercase.
    idevaluacion = models.ForeignKey(Evaluacion, models.DO_NOTHING, db_column='IDEVALUACION')  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='IDUSUARIO')  # Field name made lowercase.
    nombreplandes = models.CharField(db_column='NOMBREPLANDES', max_length=255)  # Field name made lowercase.
    objetivosplandes = models.CharField(db_column='OBJETIVOSPLANDES', max_length=255)  # Field name made lowercase.
    alcancesplandes = models.CharField(db_column='ALCANCESPLANDES', max_length=255)  # Field name made lowercase.
    descripcionplandes = models.CharField(db_column='DESCRIPCIONPLANDES', max_length=2000)  # Field name made lowercase.
    instruccionesplandes = models.CharField(db_column='INSTRUCCIONESPLANDES', max_length=2000)  # Field name made lowercase.
    duracionmesesplandes = models.IntegerField(db_column='DURACIONMESESPLANDES')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'plandesarrollo'


class Recordatorio(models.Model):
    idrecordatorio = models.AutoField(db_column='IDRECORDATORIO', primary_key=True)  # Field name made lowercase.
    idactividad = models.ForeignKey(Actividades, db_column='IDACTIVIDAD', on_delete=models.CASCADE)  # Field name made lowercase.
    nombrerecordatorio = models.CharField(db_column='NOMBRERECORDATORIO', max_length=255)  # Field name made lowercase.
    descripcionrecordatorio = models.CharField(db_column='DESCRIPCIONRECORDATORIO', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    fecharecordatorio = models.DateTimeField(db_column='FECHARECORDATORIO')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'recordatorio'


class Servicios(models.Model):
    idservicio = models.AutoField(db_column='IDSERVICIO', primary_key=True)
    iddepartamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='IDDEPARTAMENTO')
    nombreservicio = models.CharField(db_column='NOMBRESERVICIO', max_length=255)
    descripcionservicio = models.CharField(db_column='DESCRIPCIONSERVICIO', max_length=2000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'servicios'
        
    def __str__(self):
        return self.nombreservicio 


class TipoUsuario(models.Model):
    idtipousuario = models.AutoField(db_column='IDTIPOUSUARIO', primary_key=True)
    descripcion = models.CharField(db_column='DESCRIPCION', max_length=255)

    class Meta:
        managed = True
        db_table = 'tipousuario'

    def __str__(self):
        return self.descripcion

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, tipousuario=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email')
        email = self.normalize_email(email)
        
        if tipousuario is not None:
            try:
                TipoUsuarioModel = self.model._meta.get_field('tipousuario').remote_field.model
                tipousuario = TipoUsuarioModel.objects.get(pk=tipousuario)
            except TipoUsuarioModel.DoesNotExist:
                raise ValueError('TipoUsuario no válido')

        user = self.model(email=email, tipousuario=tipousuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, tipousuario=1, **extra_fields):
        return self.create_user(email, password, tipousuario=tipousuario, **extra_fields)

class Usuario(AbstractBaseUser):
    idusuario = models.AutoField(db_column='IDUSUARIO', primary_key=True)
    idservicio = models.ForeignKey('Servicios', models.DO_NOTHING, db_column='IDSERVICIO', blank=True, null=True)
    idplandes = models.ForeignKey('Plandesarrollo', models.DO_NOTHING, db_column='IDPLANDES', blank=True, null=True)
    tipousuario = models.ForeignKey(TipoUsuario, models.DO_NOTHING, db_column='IDTIPOUSUARIO')  # Actualizado
    nombre = models.CharField(db_column='NOMBRE', max_length=255)
    apellido = models.CharField(db_column='APELLIDO', max_length=255)
    dui = models.CharField(db_column='DUI', max_length=9)
    telefono = models.IntegerField(db_column='TELEFONO')
    salario = models.DecimalField(db_column='SALARIO', max_digits=10, decimal_places=0)
    email = models.EmailField(db_column='EMAIL', max_length=255, unique=True)
    password = models.CharField(db_column='PASSWORD', max_length=255)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    objects = UsuarioManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'dui', 'telefono', 'salario', 'tipousuario']

    class Meta:
        managed = True
        db_table = 'usuario'

    def __str__(self):
        return self.email