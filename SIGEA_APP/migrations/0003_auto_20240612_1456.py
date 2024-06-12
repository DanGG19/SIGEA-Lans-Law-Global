from django.db import migrations

def create_tipo_usuario(apps, schema_editor):
    TipoUsuario = apps.get_model('SIGEA_APP', 'TipoUsuario')
    TipoUsuario.objects.create(idtipousuario=1, descripcion='Administrador')
    TipoUsuario.objects.create(idtipousuario=2, descripcion='Secretaria')
    TipoUsuario.objects.create(idtipousuario=3, descripcion='Jefe de Departamento')
    TipoUsuario.objects.create(idtipousuario=4, descripcion='Abogado')

class Migration(migrations.Migration):

    dependencies = [
        ('SIGEA_APP', '0002_tipousuario_alter_usuario_tipousuario'),
    ]

    operations = [
        migrations.RunPython(create_tipo_usuario),
    ]
