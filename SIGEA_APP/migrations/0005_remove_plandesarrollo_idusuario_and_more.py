# Generated by Django 5.0.4 on 2024-06-15 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SIGEA_APP', '0004_plandesarrollo_amenazas_plandesarrollo_debilidades_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plandesarrollo',
            name='idusuario',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='idplandes',
        ),
    ]