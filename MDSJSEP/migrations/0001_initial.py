# Generated by Django 5.0.4 on 2024-04-17 22:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventosCreados',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('dia', models.DateTimeField(blank=True, null=True)),
                ('hora_inicio', models.TimeField(blank=True, null=True)),
                ('hora_finalizacion', models.TimeField(blank=True, null=True)),
                ('sala', models.CharField(blank=True, choices=[('AUDITORIO CENTRO SEP (capacidad: 220, Nivel-0)', 'AUDITORIO CENTRO SEP (capacidad: 220, Nivel-0)'), ('ESTUDIO DE GRABACIÓN (capacidad: 10, Nivel-0)', 'ESTUDIO DE GRABACIÓN (capacidad: 10, Nivel-0)'), ('BODEGA DGTIC-DGRMyS (capacidad: 20, Nivel-0)', 'BODEGA DGTIC-DGRMyS (capacidad: 20, Nivel-0)'), ('ÁREA ACTIVIDAD FISICA (capacidad: 50, Nivel-1)', 'ÁREA ACTIVIDAD FISICA (capacidad: 50, Nivel-1)'), ('CAPACITACIÓN (capacidad: 25, Nivel: 1, Sala: 1)', 'CAPACITACIÓN (capacidad: 25, Nivel: 1, Sala: 1)'), ('CAPACITACIÓN (capacidad: 25, Nivel: 1-H, Sala: 2)', 'CAPACITACIÓN (capacidad: 25, Nivel: 1-H, Sala: 2)'), ('CAPACITACIÓN (ESPEJOS) (capacidad: 25, Nivel: 1-H, Sala: 1)', 'CAPACITACIÓN (ESPEJOS) (capacidad: 25, Nivel: 1-H, Sala: 1)'), ('COMPUTO (capacidad: 20, Nivel: 1-H, Sala: 1)', 'COMPUTO (capacidad: 20, Nivel: 1-H, Sala: 1)'), ('COMPUTO (capacidad: 20, Nivel: 1-H, Sala: 2)', 'COMPUTO (capacidad: 20, Nivel: 1-H, Sala: 2)'), ('COMPUTO (capacidad: 20, Nivel: 1-H, Sala: 3)', 'COMPUTO (capacidad: 20, Nivel: 1-H, Sala: 3)'), ('SALA MEXICO (capacidad: 60, Nivel: 1-H)', 'SALA MEXICO (capacidad: 60, Nivel: 1-H)'), ('ANEXO SALA MEXICO (capacidad: 30, Nivel: 1-H)', 'ANEXO SALA MEXICO (capacidad: 30, Nivel: 1-H)'), ('ACCESO MAYORASGO (capacidad: 100, Nivel: 1)', 'ACCESO MAYORASGO (capacidad: 100, Nivel: 1)'), ('ACCESO UNIVERSIDAD 1200 LADO NORTE (capacidad: 100, Nivel: 1)', 'ACCESO UNIVERSIDAD 1200 LADO NORTE (capacidad: 100, Nivel: 1)'), ('ALA SUR (capacidad: 50, Nivel: 1)', 'ALA SUR (capacidad: 50, Nivel: 1)'), ('JAIME TORRES BODET (capacidad: 50, Nivel: 2, Sala: 1)', 'JAIME TORRES BODET (capacidad: 50, Nivel: 2, Sala: 1)'), ('NARCISO BASSOLS (capacidad: 35, Nivel: 2, Sala: 2)', 'NARCISO BASSOLS (capacidad: 35, Nivel: 2, Sala: 2)'), ('GREGORIO TORRES QUINTERO (capacidad: 20, Nivel: 2, Sala: 3)', 'GREGORIO TORRES QUINTERO (capacidad: 20, Nivel: 2, Sala: 3)'), ('ROSARIO CASTELLANOS (capacidad: 18, Nivel: 2, Sala: 4)', 'ROSARIO CASTELLANOS (capacidad: 18, Nivel: 2, Sala: 4)'), ('ANTONIO CASO (capacidad: 25, Nivel: 2, Sala: 5)', 'ANTONIO CASO (capacidad: 25, Nivel: 2, Sala: 5)'), ('JÓSE VASCONCELOS (capacidad: 60, Nivel: 2, Sala: 6)', 'JÓSE VASCONCELOS (capacidad: 60, Nivel: 2, Sala: 6)'), ('SOR JUANA INES DE LA CRUZ (capacidad: 30, Nivel: 2, Sala: 7)', 'SOR JUANA INES DE LA CRUZ (capacidad: 30, Nivel: 2, Sala: 7)'), ('JUAN JOSE ARREOLA (capacidad: 9, Nivel: 2, Sala: 9)', 'JUAN JOSE ARREOLA (capacidad: 9, Nivel: 2, Sala: 9)'), ('FRIDA KHALO (capacidad: 15, Nivel: 2, Sala: 10)', 'FRIDA KHALO (capacidad: 15, Nivel: 2, Sala: 10)'), ('JUSTO SIERRA (capacidad: 15, Nivel: 2, Sala: 11)', 'JUSTO SIERRA (capacidad: 15, Nivel: 2, Sala: 11)'), ('SALA SIN NOMBRE (capacidad: 20, Nivel: 2, Sala: 12)', 'SALA SIN NOMBRE (capacidad: 20, Nivel: 2, Sala: 12)'), ('SALA SIN NOMBRE (capacidad: 15, Nivel: 2, Sala: 13)', 'SALA SIN NOMBRE (capacidad: 15, Nivel: 2, Sala: 13)'), ('AUDITIRES (capacidad: 10, Nivel: 2, Sala: 15)', 'AUDITIRES (capacidad: 10, Nivel: 2, Sala: 15)'), ('AUDITORES (capacidad: 6, Nivel: 2, Sala: 16)', 'AUDITORES (capacidad: 6, Nivel: 2, Sala: 16)'), ('SALA SIN NOMBRE (capacidad: 30, Nivel: 2, Sala: 17)', 'SALA SIN NOMBRE (capacidad: 30, Nivel: 2, Sala: 17)'), ('SALA SIN NOMBRE (capacidad: 30, Nivel: 2, Sala: 18)', 'SALA SIN NOMBRE (capacidad: 30, Nivel: 2, Sala: 18)'), ('SALA SIN NOMBRE (capacidad: 30, Nivel: 2, Sala: 19)', 'SALA SIN NOMBRE (capacidad: 30, Nivel: 2, Sala: 19)'), ('SALA SIN NOMBRE (capacidad: 15, Nivel: 2, Sala: 20)', 'SALA SIN NOMBRE (capacidad: 15, Nivel: 2, Sala: 20)'), ('"EJCUTIVA" (capacidad: 10, Nivel: 2, Sala: A)', '"EJCUTIVA" (capacidad: 10, Nivel: 2, Sala: A)'), ('"EJCUTIVA" (capacidad: 10, Nivel: 2, Sala: B)', '"EJCUTIVA" (capacidad: 10, Nivel: 2, Sala: B)'), ('"EJCUTIVA" (capacidad: 10, Nivel: 2, Sala: C)', '"EJCUTIVA" (capacidad: 10, Nivel: 2, Sala: C)'), ('"EJCUTIVA" (capacidad: 10, Nivel: 2, Sala: D)', '"EJCUTIVA" (capacidad: 10, Nivel: 2, Sala: D)'), ('INTERNA (capacidad: 12, Nivel: 5, Sala: 5.18)', 'INTERNA (capacidad: 12, Nivel: 5, Sala: 5.18)'), ('SALA SIN NOMBRE (capacidad: 25, Nivel: 5, Sala: 5-G)', 'SALA SIN NOMBRE (capacidad: 25, Nivel: 5, Sala: 5-G)'), ('AUDITORIO REVOLUCIÓN 1425 (capacidad: 220)', 'AUDITORIO REVOLUCIÓN 1425 (capacidad: 220)'), ('SALA DGP REVOLUCIÓN 1425 (capacidad: 100)', 'SALA DGP REVOLUCIÓN 1425 (capacidad: 100)'), ('MEZZANNINE REVOLUCIÓN 1425 (capacidad: 100)', 'MEZZANNINE REVOLUCIÓN 1425 (capacidad: 100)'), ('SALA VIADUCTO 551 (capacidad: 50)', 'SALA VIADUCTO 551 (capacidad: 50)'), ('RABOSO (PUEBLA) (capacidad: 15, Sala: 1)', 'RABOSO (PUEBLA) (capacidad: 15, Sala: 1)'), ('RABOSO (PUEBLA) (capacidad: 15, Sala: 2)', 'RABOSO (PUEBLA) (capacidad: 15, Sala: 2)'), ('RABOSO (PUEBLA) (capacidad: 15, Sala: 3)', 'RABOSO (PUEBLA) (capacidad: 15, Sala: 3)'), ('RABOSO (PUEBLA) (capacidad: 15, Sala: 4)', 'RABOSO (PUEBLA) (capacidad: 15, Sala: 4)'), ('RABOSO (PUEBLA) (capacidad: 15, Sala: 5)', 'RABOSO (PUEBLA) (capacidad: 15, Sala: 5)')], max_length=100, null=True)),
                ('prioridad', models.CharField(blank=True, choices=[('Alta', 'Alta'), ('Media', 'Media'), ('Baja', 'Baja')], max_length=10, null=True)),
                ('coordina', models.CharField(blank=True, max_length=50, null=True)),
                ('preside', models.CharField(blank=True, max_length=50, null=True)),
                ('cargo', models.CharField(blank=True, max_length=50, null=True)),
                ('no_personas', models.CharField(blank=True, max_length=10, null=True)),
                ('contacto', models.CharField(blank=True, max_length=20, null=True)),
                ('servicios', models.CharField(blank=True, max_length=100, null=True)),
                ('observaciones', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
                'permissions': [('add_evento', 'Can add evento in tasks app'), ('change_evento', 'Can change evento in tasks app'), ('delete_evento', 'Can delete evento in tasks app'), ('view_evento', 'Can view evento in tasks app')],
            },
        ),
        migrations.CreateModel(
            name='Task_eventos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=200, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]