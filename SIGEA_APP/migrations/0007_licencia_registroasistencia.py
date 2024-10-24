# Generated by Django 5.0.4 on 2024-08-26 02:51

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIGEA_APP', '0006_merge_20240825_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Licencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('tipo_licencia', models.CharField(max_length=50)),
                ('dias_utilizados', models.IntegerField(default=0)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licencias', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroAsistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('hora_entrada', models.TimeField()),
                ('hora_salida', models.TimeField(blank=True, null=True)),
                ('horas_trabajadas', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros_asistencia', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]