# -*- coding: utf-8 -*-


import sys
import os
import re
import utilidades
import runpy

if sys.platform.startswith("win"):
    import msvcrt
else:
    import termios
    import tty

limpiar = "cls" if os.name == "nt" else "clear"
os.system(limpiar)

# CARGA DE DATOS
usuarios = utilidades.cargar_diccionario("usuarios")
mercado = utilidades.cargar_diccionario("mercado")
armas = utilidades.cargar_diccionario("armas")
camuflajes = utilidades.cargar_diccionario("camuflajes")
inventarios_raw = utilidades.cargar_diccionario("inventarios")

# VALIDAR SESION
try:
    with open("diccionarios/sesion.dat", "r") as archivo_sesion:
        id_usuario_ingresado = utilidades.cargar_diccionario("sesion")
        nombre_usuario = usuarios[id_usuario_ingresado][0]
        sesion_iniciada = True
except:
    sesion_iniciada = False
    nombre_usuario = ""
    id_usuario_ingresado = None

# INVENTARIO DEL USUARIO
inventario_completo = {}
for claves, cantidad in inventarios_raw.items():
    id_usuario, id_camuflaje, id_arma = claves
    if id_usuario == id_usuario_ingresado:
        nombre_camuflaje, rareza, precio_camuflaje, _ = camuflajes[id_camuflaje]
        nombre_arma, precio_arma, _ = armas[id_arma]
        nombre_completo = nombre_arma + " con " + nombre_camuflaje
        precio_final = precio_arma + precio_camuflaje
        inventario_completo[(id_camuflaje, id_arma)] = [nombre_completo, precio_final, rareza, cantidad]

#PARA VOLVER AL MENU
def esperar():
    input("\nPresione ENTER para volver al menu del mercado...")

# Menú del Mercado
opciones_menu = [
    "[0] Volver al menu principal",
    "[1] Armas en venta",
    "[2] Agregar un arma al mercado",
    "[3] Eliminar un arma del mercado"
]

while True:
    opcion_seleccionada = 0
    menu_activo = True

    while menu_activo:
        os.system(limpiar)
        print("<<<<<<<<<<<<<<<<<<< Mercado >>>>>>>>>>>>>>>>>>>")
        print("\nUse las flechas para moverse y ENTER para seleccionar:\n")

        if sesion_iniciada:
            print("\nSesion iniciada como:", nombre_usuario, "\n")
        else:
            print("\nSesion no iniciada, por favor diríjase a la gestión de usuarios\n")

        for indice, texto in enumerate(opciones_menu):
            prefijo = "\033[92m> \033[0m" if indice == opcion_seleccionada else "  "
            print(prefijo + texto)

        print("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        # Captura de teclas
        if sys.platform.startswith("win"):
            tecla = utilidades._leer_tecla_windows()
            if tecla == '\xe0':
                tecla = utilidades._leer_tecla_windows()
                if tecla == 'H':
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones_menu)
                elif tecla == 'P':
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones_menu)
            elif tecla == '\r':
                menu_activo = False
        else:
            entrada = sys.stdin.fileno()
            configuracion_anterior = termios.tcgetattr(entrada)
            tty.setraw(entrada)
            tecla1 = sys.stdin.read(1)
            if tecla1 == '\x1b':
                sys.stdin.read(1)
                tecla3 = sys.stdin.read(1)
                if tecla3 == 'A':
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones_menu)
                elif tecla3 == 'B':
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones_menu)
            elif tecla1 == '\n':
                menu_activo = False
            termios.tcsetattr(entrada, termios.TCSADRAIN, configuracion_anterior)

    # OPCIONES DEL MENU
    if opcion_seleccionada == 0:
        os.system(limpiar)
        print("\033[92mVolviendo al menu principal...\033[0m\n")
        runpy.run_path("menu_principal.py")
        break
#OPCION 1 (BUSCAR Y COMPRAR ARMAS)
    elif opcion_seleccionada == 1:
        os.system(limpiar)
        print(">> Buscar un arma en el mercado\n")

        if not mercado:
            print("No hay armas en el mercado.")
            esperar()
        else:
            # ARMAS DISPONIBLES
            for id_pub, datos in mercado.items():
                arma = armas.get(datos.get("arma_id"), ["???"])
                camu = camuflajes.get(datos.get("camuflaje_id"), ["???"])
                vendedor = usuarios.get(datos.get("vendedor"), ["???"])[0]
                cantidad = datos.get("cantidad", 1)

                print("[%d] %s con %s - Precio: %d - Cantidad: %d - Vendedor: %s" % (
                    id_pub,
                    arma[0],
                    camu[0],
                    datos.get("precio", 0),
                    cantidad,
                    vendedor
                ))

            # VERIFICAR SI LA SESION ESTA ACTIVA
            if not sesion_iniciada:
                print("\nDebe iniciar sesion para comprar armas.")
                esperar()
            else:
                try:
                    eleccion = int(input("\nIngrese el ID del arma que desea comprar (0 para cancelar): "))
                except:
                    print("Entrada invalida.")
                    esperar()
                    continue

                if eleccion == 0:
                    continue

                if eleccion not in mercado:
                    print("ID de publicacion invalido.")
                    esperar()
                    continue

                publicacion = mercado[eleccion]
                precio_unitario = publicacion.get("precio", 0)
                vendedor_id = publicacion.get("vendedor")
                cantidad_disponible = publicacion.get("cantidad", 1)

                # VALIDAR
                if vendedor_id == id_usuario_ingresado:
                    print("No puedes comprar tu propia publicacion.")
                    esperar()
                    continue

                if cantidad_disponible < 1:
                    print("Esta publicacion ya no tiene unidades disponibles.")
                    esperar()
                    continue
                # PREGUNTAR CUANTAS QUIERE COMPRAR
                try:
                    cant_comprar = int(input("Cuantas desea comprar (1-%d): " % cantidad_disponible))
                except:
                    print("Entrada invalida.")
                    esperar()
                    continue

                if cant_comprar < 1 or cant_comprar > cantidad_disponible:
                    print("Cantidad invalida.")
                    esperar()
                    continue

                precio_total = precio_unitario * cant_comprar

                saldo_comprador = usuarios[id_usuario_ingresado][3]  
                if saldo_comprador < precio_total:
                    print("No tienes saldo suficiente para comprar esta arma.")
                    esperar()
                    continue

                # ENVIAR ARMA AL INVENTARIO
                clave_inventario = (id_usuario_ingresado, publicacion["camuflaje_id"], publicacion["arma_id"])
                if clave_inventario in inventarios_raw:
                    inventarios_raw[clave_inventario] += 1
                else:
                    inventarios_raw[clave_inventario] = 1

                # ACTUALIZAR SALDOS
                usuarios[id_usuario_ingresado][3] -= precio_total        #RESTA COMPRADO
                usuarios[vendedor_id][3] += precio_total                 #SUMA VENDEDOR

                arma_nombre = armas[publicacion["arma_id"]][0]
                camu_nombre = camuflajes[publicacion["camuflaje_id"]][0]

                # ACTUALIZAR VENTA O ELIMINAR EL PRODUCTO
                publicacion["cantidad"] -= cant_comprar
                if publicacion["cantidad"] <= 0:
                    del mercado[eleccion]

                # CAMBIOS GUARDADOS
                utilidades.guardar_diccionario("mercado", mercado)
                utilidades.guardar_diccionario("usuarios", usuarios)
                utilidades.guardar_diccionario("inventarios", inventarios_raw)

                # CONFIRMAION DE LA COMPRA
                print("\nCompra realizada con exito!")
                print("Has adquirido %d x %s con %s por %d" % (
                    cant_comprar,
                    arma_nombre,
                    camu_nombre,
                    precio_total
                ))
                esperar()
#OPCION 2 (AGREGAR UN ARMA AL MERCADO)
    elif opcion_seleccionada == 2:
        os.system(limpiar)
        print(">> Agregar un arma al mercado\n")
        if not sesion_iniciada:
            print("Debe iniciar sesian para vender en el mercado.")
            esperar()
            continue

        if not inventario_completo:
            print("No tienes armas en tu inventario para vender.")
            esperar()
            continue

        print("Tu inventario:\n")
        lista_items = list(inventario_completo.items())
        for idx, ((id_camuflaje, id_arma), datos) in enumerate(lista_items, start=1):
            nombre_completo, precio_final, rareza, cantidad = datos
            print("[%d] %s - Rareza: %s - Precio base: %d - Cantidad: %d" % (
                idx, nombre_completo, rareza, precio_final, cantidad
            ))

        try:
            eleccion = int(input("\nSeleccione un arma para vender: "))
            if eleccion < 1 or eleccion > len(lista_items):
                print("Opcion invalida.")
                esperar()
                continue
        except:
            print("Entrada invalida.")
            esperar()
            continue

        (id_camuflaje, id_arma), datos = lista_items[eleccion - 1]
        nombre_completo, precio_minimo, rareza, cantidad_disponible = datos

        try:
            precio = int(input("Ingrese precio de venta (minimo %d): " % precio_minimo))
            if precio < precio_minimo:
                print("El precio no puede ser menor al minimo (%d)." % precio_minimo)
                esperar()
                continue
        except:
            print("Entrada invalida.")
            esperar()
            continue

        # CANTIDAD DE UNIDADES A VENDER
        if cantidad_disponible > 1:
            try:
                cantidad_vender = int(input("Cuantas unidades deseas vender (max %d): " % cantidad_disponible))
                if cantidad_vender < 1 or cantidad_vender > cantidad_disponible:
                    print("Cantidad invalida.")
                    esperar()
                    continue
            except:
                print("Entrada invalida.")
                esperar()
                continue
        else:
            cantidad_vender = 1

        # CREAR EL NUEVO ID PARA EL PRODUCTO EN VENTA
        try:
            nuevo_id = max([int(k) for k in mercado.keys()]) + 1 if mercado else 1
        except:
            nuevo_id = 1

        mercado[int(nuevo_id)] = {
            "arma_id": id_arma,
            "camuflaje_id": id_camuflaje,
            "precio": precio,
            "cantidad": cantidad_vender,
            "vendedor": id_usuario_ingresado
        }
        utilidades.guardar_diccionario("mercado", mercado)

        # DESCONTAR O SACAR EL ARMA DEL INVENTARIO
        clave_inventario = (id_usuario_ingresado, id_camuflaje, id_arma)
        if clave_inventario in inventarios_raw:
            cantidad_actual = inventarios_raw[clave_inventario]

            if cantidad_vender >= cantidad_actual:
                del inventarios_raw[clave_inventario]
            else:
                inventarios_raw[clave_inventario] -= cantidad_vender
                
            #CAMBIOS GUARDADOS
            utilidades.guardar_diccionario("inventarios", inventarios_raw)
            print("Arma publicada en el mercado con ID:", nuevo_id)
        else:
            print("No tienes esa arma en tu inventario.")

        esperar()
#OPCION 3 (ELIMINAR UNA PUBLICACION DEL MERCADO)
    elif opcion_seleccionada == 3:
        os.system(limpiar)
        print(">> Eliminar un arma del mercado\n")

        if not sesion_iniciada:
            print("Debe iniciar sesion para eliminar publicaciones.")
            esperar()
            continue

        # FILTRAR SOLO LA PUBLICACIONES DEL USUARIO
        publicaciones = {k: v for k, v in mercado.items() if v.get("vendedor") == id_usuario_ingresado}
        if not publicaciones:
            print("No tienes armas publicadas en el mercado.")
            esperar()
            continue

        print("Tus publicaciones:\n")
        for id_pub, datos in publicaciones.items():
            arma = armas.get(datos.get("arma_id"), ["???"])[0]
            camu = camuflajes.get(datos.get("camuflaje_id"), ["???"])[0]
            print("[%d] %s con %s - Precio: %d - Cantidad: %d" % (
                id_pub, arma, camu, datos.get("precio", 0), datos.get("cantidad", 1)
            ))

        try:
            eleccion = int(input("\nSeleccione el ID de publicacion a eliminar (0 para cancelar): "))
        except:
            print("Entrada invalida.")
            esperar()
            continue

        if eleccion == 0:
            continue

        if eleccion not in publicaciones:
            print("ID invalido.")
            esperar()
            continue

        publicacion = mercado[eleccion]
        id_arma = publicacion["arma_id"]
        id_camu = publicacion["camuflaje_id"]
        cantidad = publicacion.get("cantidad", 1)

        # DEVOLUCION DEL ARMA DESDE EL MERCADO AL INVENTARIO
        clave_inventario = (id_usuario_ingresado, id_camu, id_arma)
        if clave_inventario in inventarios_raw:
            inventarios_raw[clave_inventario] += cantidad
        else:
            inventarios_raw[clave_inventario] = cantidad

        # ELIMINAR LA PUBLICACION DEL MERCADO
        del mercado[eleccion]

        # CAMBIO GUARDADOS
        utilidades.guardar_diccionario("mercado", mercado)
        utilidades.guardar_diccionario("inventarios", inventarios_raw)

        print("Publicacion eliminada correctamente y arma devuelta a tu inventario.")
        esperar()