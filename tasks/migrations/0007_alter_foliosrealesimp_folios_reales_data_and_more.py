# Generated by Django 4.2.3 on 2023-10-10 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_foliosrealesimp_folios_reales_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foliosrealesimp',
            name='folios_reales_data',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='foliosrealesimp',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folios_reales_data', to='tasks.inmueble'),
        ),
        migrations.AlterField(
            model_name='task',
            name='NombreInmueble',
            field=models.CharField(max_length=200, null=True, verbose_name='Nombre del inmueble'),
        ),
    ]