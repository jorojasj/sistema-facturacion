# Generated by Django 3.1.2 on 2024-07-17 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_entrega_motivorechazo'),
    ]

    operations = [
        migrations.AddField(
            model_name='motivorechazo',
            name='orden_compra',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='motivos_rechazo', to='app.ordencompra'),
        ),
    ]
