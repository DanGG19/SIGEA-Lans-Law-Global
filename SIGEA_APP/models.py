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
    idactividad = models.ForeignKey(Actividades, models.DO_NOTHING, db_column='IDACTIVIDAD')  # Field name made lowercase.
    nombrerecordatorio = models.CharField(db_column='NOMBRERECORDATORIO', max_length=255)  # Field name made lowercase.
    descripcionrecordatorio = models.CharField(db_column='DESCRIPCIONRECORDATORIO', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    fecharecordatorio = models.DateTimeField(db_column='FECHARECORDATORIO')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'recordatorio'


class Servicios(models.Model):
    idservicio = models.AutoField(db_column='IDSERVICIO', primary_key=True)  # Field name made lowercase.
    iddepartamento = models.ForeignKey(Departamentos, models.DO_NOTHING, db_column='IDDEPARTAMENTO')  # Field name made lowercase.
    nombreservicio = models.CharField(db_column='NOMBRESERVICIO', max_length=255)  # Field name made lowercase.
    descripcionservicio = models.CharField(db_column='DESCRIPCIONSERVICIO', max_length=2000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'servicios'


    
class UsuarioManager(BaseUserManager): # BaseUserManager es una clase que se encarga de manejar la creación de usuarios
    def create_user(self, email, password=None, **extra_fields):
        if not email: # Si no se ingresa un email, se lanza un error
            raise ValueError('El usuario debe tener un email') # ValueError es una excepción que se lanza cuando un valor es incorrecto
        email = self.normalize_email(email) # normalize_email es un método que se encarga de normalizar el email (convertirlo a minúsculas)
        user = self.model(email=email, **extra_fields) # Se crea un usuario con el email normalizado y los campos extra que se pasen como argumento en el método
        user.set_password(password) # Se encripta la contraseña del usuario con el método set_password de django
        user.save(using=self._db) # Se guarda el usuario en la base de datos
        return user # Se retorna el usuario creado

    def create_superuser(self, email, password=None, **extra_fields): # Método para crear un superusuario
        return self.create_user(email, password, **extra_fields) # Se llama al método create_user para crear un superusuario

class Usuario(AbstractBaseUser): # AbstractBaseUser es una clase que se encarga de manejar la autenticación de los usuarios
    idusuario = models.AutoField(db_column='IDUSUARIO', primary_key=True)  # Field name made lowercase.
    idservicio = models.ForeignKey('Servicios', models.DO_NOTHING, db_column='IDSERVICIO', blank=True, null=True)  # Field name made lowercase.
    idplandes = models.ForeignKey('Plandesarrollo', models.DO_NOTHING, db_column='IDPLANDES', blank=True, null=True)  # Field name made lowercase.
    tipousuario = models.IntegerField(db_column='TIPOUSUARIO')  # Field name made lowercase.
    nombre = models.CharField(db_column='NOMBRE', max_length=255)  # Field name made lowercase.
    apellido = models.CharField(db_column='APELLIDO', max_length=255)  # Field name made lowercase.
    dui = models.CharField(db_column='DUI', max_length=9)  # Field name made lowercase.
    telefono = models.IntegerField(db_column='TELEFONO')  # Field name made lowercase.
    salario = models.DecimalField(db_column='SALARIO', max_digits=10, decimal_places=0)  # Field name made lowercase.
    email = models.EmailField(db_column='EMAIL', max_length=255, unique=True)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=255) # Field name made lowercase.
    
    objects = UsuarioManager() # Se asigna el manager de Usuario a la variable objects
    USERNAME_FIELD = 'email' # Se asigna el campo email como campo de autenticación
    REQUIRED_FIELDS = ['nombre', 'apellido', 'dui', 'telefono', 'salario', 'tipousuario'] # Se asignan los campos requeridos para la creación de un usuario

    class Meta: # Metaclase para configurar el modelo Usuario en la base de datos 
        managed = True # Se indica que el modelo es gestionado por Django
        db_table = 'usuario' # Se asigna el nombre de la tabla en la base de datos
            
    def __str__(self): # Método para retornar el email del usuario como representación del objeto en string 
        return self.email # Se retorna el email del usuario 
