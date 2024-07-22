# Generated by Django 5.0.4 on 2024-07-11 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIGEA_APP', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='dui',
            field=models.CharField(db_column='DUI', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.IntegerField(db_column='TELEFONO', max_length=9, unique=True),
        ),
    ]