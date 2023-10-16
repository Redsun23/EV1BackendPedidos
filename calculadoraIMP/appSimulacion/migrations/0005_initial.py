# Generated by Django 4.2.5 on 2023-10-08 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appSimulacion', '0004_delete_pedido'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_ud', models.PositiveIntegerField()),
                ('costo_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nombre_articulo', models.CharField(max_length=255)),
                ('codigo_articulo', models.CharField(max_length=46)),
                ('nombre_proveedor', models.CharField(max_length=50)),
                ('costo_envio_usd', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_pedido_clp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('costo_envio_clp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('impuesto_aduana_clp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('iva_clp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_impuestos_aduana_clp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('costo_total_compra_usd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('costo_total_compra_clp', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
