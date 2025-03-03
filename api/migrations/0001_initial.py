# Generated by Django 5.0.12 on 2025-02-26 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('concepto', models.CharField(max_length=200)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.empleado')),
            ],
        ),
    ]
