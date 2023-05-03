# Generated by Django 4.2 on 2023-05-01 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(default=2, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('contrasena', models.CharField(max_length=128)),
                ('tipo_cuenta', models.CharField(max_length=10)),
            ],
        ),
    ]