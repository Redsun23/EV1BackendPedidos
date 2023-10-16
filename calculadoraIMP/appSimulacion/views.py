from django.shortcuts import render, redirect
from .models import Pedido, Resultados

#funcion para listar pedidos
def PedidosData(request):
    pedidos = Pedido.objects.all()
    data = {'pedidos': pedidos}
    return render(request, 'ListaSimulaciones.html', data)

#Fucion para mostrar los resultdos
def Mostrar_resultado(request, pedido_id):
    # Obtener el pedido por su ID
    pedido = Pedido.objects.get(pk= pedido_id)
    #obtener el resultado asociado a ese pedido
    resultado = Resultados.objects.get(pedido=pedido)
    data = {'pedido': pedido, 'resultado': resultado}
    return render(request, 'Mostrar_resultado.html', data)

#funcion para eliminar pedidos
def eliminar_pedido(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    if request.method == 'GET':
        return render(request, 'EliminarPedido.html', {'pedido': pedido})
    elif request.method == 'POST':
        pedido.delete()
        return redirect('home')


def actualizar_pedido(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    if request.method == 'POST':
        # Procesar el formulario enviado
        cantidad_ud = int(request.POST['cantidad_ud'])
        costo_unitario = float(request.POST['costo_unitario'])
        costo_envio_usd = float(request.POST['costo_envio_usd'])
        # Realizar los cálculos 
        valores_calculados = calcular_valores_pedido(cantidad_ud, costo_unitario, costo_envio_usd)
        # Actualizar los campos del pedido
        pedido.cantidad_ud = cantidad_ud
        pedido.costo_unitario_usd = costo_unitario
        pedido.costo_envio_usd = costo_envio_usd
        # Guardar los cambios en el pedido
        pedido.save()
        # Obtener el objeto Resultados relacionado con el pedido
        resultados = Resultados.objects.get(pedido=pedido)
        # Asignar los valores calculados a los campos de resultados
        resultados.total_pedido_clp = valores_calculados['total_pedido_clp']
        resultados.costo_envio_clp = valores_calculados['costo_envio_clp']
        resultados.impuesto_aduana_clp = valores_calculados['impuesto_aduana_clp']
        resultados.iva_clp = valores_calculados['iva_clp']
        resultados.total_impuestos_aduana_clp = valores_calculados['total_impuestos_aduana_clp']
        resultados.costo_total_compra_usd = valores_calculados['costo_total_compra_usd']
        resultados.costo_total_compra_clp = valores_calculados['costo_total_compra_clp']
        # Guardar los resultados en la base de datos
        resultados.save()
        # Redirigir a la página de detalle del pedido actualizado o a donde desees
        return redirect('home')
    data = {'pedido': pedido}
    # Si la solicitud no es POST, mostrar el formulario de edición
    return render(request, 'ActualizarPedido.html', data)

# Aplicar la Ley de Redondeo de Chile
def redondear_chile(valor):
    decimal_part = valor - int(valor)
    if decimal_part in [0.1, 0.2, 0.6, 0.7]:#Si decimal_part es igual a 0.1, 0.2, 0.6 o 0.7, se redondea hacia abajo 
        valor_redondeado = int(valor)
    elif decimal_part in [0.3, 0.4, 0.8, 0.9]:#Si decimal_part es igual a 0.3, 0.4, 0.8 o 0.9, se redondea hacia arriba
        valor_redondeado = int(valor) + 1
    else:#Si decimal_part no coincide con ninguno de estos valores, se redondea hacia abajo, lo que significa que se trunca a la parte entera.
        valor_redondeado = int(valor)

    return valor_redondeado

def calcular_valores_pedido(cantidad_ud, costo_unitario, costo_envio_usd):
    #calcular los valores  para clp y valor cif en usd
    total_pedido_usd = cantidad_ud * costo_unitario
    total_pedido_clp = total_pedido_usd * 890
    costo_envio_clp = costo_envio_usd * 890
    valor_cif_usd = total_pedido_usd + costo_envio_usd
    #calculo para los impuestos/6%CIF, iva 19% , total de impuestos
    impuesto_aduana_clp = valor_cif_usd * 0.06 * 890
    iva_clp = valor_cif_usd * 0.19 * 890
    total_impuestos_aduana_clp = impuesto_aduana_clp + iva_clp
    #calculo para el total de la compra en clp y usd
    costo_total_compra_clp = total_pedido_clp + costo_envio_clp + total_impuestos_aduana_clp
    costo_total_compra_usd = costo_total_compra_clp / 890

    # Aplicar redondeo de Chile a los valores
    total_pedido_clp = redondear_chile(total_pedido_clp)
    costo_envio_clp = redondear_chile(costo_envio_clp)
    impuesto_aduana_clp = redondear_chile(impuesto_aduana_clp)
    iva_clp = redondear_chile(iva_clp)
    total_impuestos_aduana_clp = redondear_chile(total_impuestos_aduana_clp)
    costo_total_compra_clp = redondear_chile(costo_total_compra_clp)

    return {
        "total_pedido_clp": total_pedido_clp,
        "costo_envio_clp": costo_envio_clp,
        "impuesto_aduana_clp": impuesto_aduana_clp,
        "iva_clp": iva_clp,
        "total_impuestos_aduana_clp": total_impuestos_aduana_clp,
        "costo_total_compra_usd": costo_total_compra_usd,
        "costo_total_compra_clp": costo_total_compra_clp
    }


#funcion agregar para agrega pedido
def AgregarPedido(request):
    if request.method == 'POST':
        cantidad_ud = int(request.POST['cantidad_unidades'])
        costo_unitario= float(request.POST['costo_unitario'])
        costo_envio_usd = float(request.POST['costo_envio_usd'])
        nombre_articulo = request.POST['nombre_articulo']
        codigo_articulo = request.POST['codigo_articulo']
        nombre_proveedor = request.POST['nombre_proveedor']
        #se llama a la funcion para calcular los valores
        valores_calculados = calcular_valores_pedido(cantidad_ud, costo_unitario, costo_envio_usd)
        # Crear una instancia de Pedido y Resultados con los valores calculados
        pedido = Pedido(
            cantidad_ud = cantidad_ud,
            costo_unitario = costo_unitario,
            nombre_articulo = nombre_articulo,
            codigo_articulo = codigo_articulo,
            nombre_proveedor = nombre_proveedor,
            costo_envio_usd = costo_envio_usd
        )
        pedido.save()
        
        resultados = Resultados(
            total_pedido_clp=valores_calculados['total_pedido_clp'],
            costo_envio_clp=valores_calculados['costo_envio_clp'],
            impuesto_aduana_clp=valores_calculados['impuesto_aduana_clp'],
            iva_clp=valores_calculados['iva_clp'],
            total_impuestos_aduana_clp=valores_calculados['total_impuestos_aduana_clp'],
            costo_total_compra_usd=valores_calculados['costo_total_compra_usd'],
            costo_total_compra_clp=valores_calculados['costo_total_compra_clp'],
            pedido=pedido  # Asociar este resultado con el pedido
        )
        resultados.save()

        return redirect('home')
    return render(request, 'CrearSimulacion.html')


