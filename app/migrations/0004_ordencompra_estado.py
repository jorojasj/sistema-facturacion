# Generated by Django 3.1.2 on 2024-07-04 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20240605_0302'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordencompra',
            name='estado',
            field=models.CharField(choices=[('creada', 'Creada'), ('rectificada', 'Rectificada')], default='creada', max_length=11),
        ),
    ]