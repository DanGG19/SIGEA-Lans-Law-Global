# Generated by Django 5.0.4 on 2024-07-11 03:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIGEA_APP', '0003_alter_usuario_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitados_actividad',
            name='idactividad',
            field=models.ForeignKey(db_column='IDACTIVIDAD', on_delete=django.db.models.deletion.CASCADE, to='SIGEA_APP.actividades'),
        ),
        migrations.AlterField(
            model_name='invitados_actividad',
            name='idusuario',
            field=models.ForeignKey(db_column='IDUSUARIO', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
