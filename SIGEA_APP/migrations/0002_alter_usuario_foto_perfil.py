# Generated by Django 5.0.4 on 2024-11-10 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIGEA_APP', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='foto_perfil',
            field=models.ImageField(blank=True, default='fotos_perfil/perfil-del-usuario.png', null=True, upload_to='fotos_perfil/'),
        ),
    ]