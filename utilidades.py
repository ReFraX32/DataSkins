# -*- coding: utf-8 -*-


import sys
import os

if os.name == "nt":
    import msvcrt
    termios = None
    tty = None
else:
    import termios
    import tty

limpiar = "cls" if os.name == "nt" else "clear"

def _leer_tecla_windows():
    k = msvcrt.getch()
    if isinstance(k, bytes):
        try:
            return k.decode('latin-1')
        except Exception:
            return chr(k[0])
    return k

def mostrar_menu(titulo, opciones, sesion_iniciada=None, nombre_usuario=""):
    opcion_seleccionada = 0
    menu_activo = True

    while menu_activo:
        os.system(limpiar)
        print("<<<<<<<<<<<<<<<<<<< " + titulo + " >>>>>>>>>>>>>>>>>>>")
        print("\nUse las flechas para moverse y ENTER para seleccionar:\n")

        if sesion_iniciada:
            print("\nSesion iniciada como:", nombre_usuario, "\n")
        elif not sesion_iniciada and sesion_iniciada != None:
            print("\nSesion no iniciada.\n")

        for indice in range(len(opciones)):
            if indice == opcion_seleccionada:
                print("\033[92m> \033[0m" + opciones[indice])
            else:
                print("  " + opciones[indice])

        print("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        if sys.platform.startswith("win"):
            tecla = _leer_tecla_windows()
            if tecla == '\xe0':
                tecla = _leer_tecla_windows()
                if tecla == 'H':  # Flecha arriba
                    opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                elif tecla == 'P':  # Flecha abajo
                    opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
            elif tecla == '\r':  # ENTER
                menu_activo = False
        else:
            entrada = sys.stdin.fileno()
            configuracion_anterior = termios.tcgetattr(entrada)
            try:
                tty.setraw(entrada)
                tecla1 = sys.stdin.read(1)

                if tecla1 == '\x1b':  # Secuencias que empiezan con ESC
                    tecla2 = sys.stdin.read(1)
                    tecla3 = sys.stdin.read(1)

                    if tecla2 == '[':
                        if tecla3 == 'A':  # Flecha arriba
                            opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
                        elif tecla3 == 'B':  # Flecha abajo
                            opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)

                    elif tecla2 == 'O' and tecla3 == 'M':  # Enter del keypad
                        menu_activo = False

                elif tecla1 in ('\n', '\r'):  # Enter
                    menu_activo = False

            finally:
                termios.tcsetattr(entrada, termios.TCSADRAIN, configuracion_anterior)

    return opcion_seleccionada

def mostrar_menu_cajas(titulo, lista):
    indice_seleccionado = 0
    while True:
        os.system(limpiar)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<< " + titulo + " >>>>>>>>>>>>>>>>>>>>>>")
        print("\n  Nombre:", "\t| Descripcion:", "\t| Precio:")
        for i in range(len(lista)):
            texto = lista[i][1]
            if i == indice_seleccionado:
                print("\033[92m> \033[0m" + texto)
            else:
                print("  " + texto)
        print("\nSeleccione con las flechas y presione ENTER:\n")
        print("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        # Windows
        if sys.platform.startswith("win"):
            tecla = _leer_tecla_windows()
            if tecla == '\xe0':
                tecla = _leer_tecla_windows()
                if tecla == 'H':  # arriba
                    indice_seleccionado = (indice_seleccionado - 1) % len(lista)
                elif tecla == 'P':  # abajo
                    indice_seleccionado = (indice_seleccionado + 1) % len(lista)
            elif tecla == '\r':  # Enter
                return indice_seleccionado

        # Linux / Mac
        else:
            entrada = sys.stdin.fileno()
            configuracion_anterior = termios.tcgetattr(entrada)
            try:
                tty.setraw(entrada)
                tecla1 = sys.stdin.read(1)

                if tecla1 == '\x1b':  # ESC
                    tecla2 = sys.stdin.read(1)
                    tecla3 = sys.stdin.read(1)
                    if tecla2 == '[':
                        if tecla3 == 'A':  # arriba
                            indice_seleccionado = (indice_seleccionado - 1) % len(lista)
                        elif tecla3 == 'B':  # abajo
                            indice_seleccionado = (indice_seleccionado + 1) % len(lista)
                    elif tecla2 == 'O' and tecla3 == 'M':
                        return indice_seleccionado
                elif tecla1 in ('\n', '\r'):
                    return indice_seleccionado
            finally:
                termios.tcsetattr(entrada, termios.TCSADRAIN, configuracion_anterior)

def mostrar_menu_filtrado(titulo, inventario, opciones_filtros, tipo, regex_color=None, orden_rareza=None):
    opcion_filtro = 0
    menu_activo = True

    while menu_activo:
        os.system(limpiar)
        print("<<<<<<<<<<<<<<<<<<<<<< " + titulo + " >>>>>>>>>>>>>>>>>>>>>>>>")

        if tipo == "completo" or tipo == "camuflajes":
            print("Nombre:", "\t| Precio:", "\t| Rareza:", "\t| Cantidad:")
        elif tipo == "armas":
            print("Nombre:", "\t| Precio:", "\t| Cantidad:")

        datos_ordenados = []

        for clave, datos in inventario.items():
            if tipo == "completo":
                nombre, precio, rareza, cantidad = datos
                nombre_limpio = regex_color.sub('', nombre)
                rareza_limpia = regex_color.sub('', rareza)

                if opcion_filtro in (0, 1):  # Nombre
                    datos_ordenados.append((nombre_limpio, nombre, precio, rareza, cantidad))
                elif opcion_filtro in (2, 3):  # Precio
                    datos_ordenados.append((precio, nombre, rareza, cantidad))
                elif opcion_filtro in (4, 5):  # Rareza
                    datos_ordenados.append((orden_rareza.index(rareza_limpia), nombre, precio, rareza, cantidad))
                elif opcion_filtro in (6, 7):  # Cantidad
                    datos_ordenados.append((cantidad, nombre, precio, rareza))

            elif tipo == "camuflajes":
                nombre, precio, rareza, cantidad = datos
                nombre_limpio = regex_color.sub('', nombre)
                rareza_limpia = regex_color.sub('', rareza)

                if opcion_filtro in (0, 1):  # Nombre
                    datos_ordenados.append((nombre_limpio, nombre, precio, rareza, cantidad))
                elif opcion_filtro in (2, 3):  # Precio
                    datos_ordenados.append((precio, nombre, rareza, cantidad))
                elif opcion_filtro in (4, 5):  # Rareza
                    datos_ordenados.append((orden_rareza.index(rareza_limpia), nombre, precio, rareza, cantidad))
                elif opcion_filtro in (6, 7):  # Cantidad
                    datos_ordenados.append((cantidad, nombre, precio, rareza))

            elif tipo == "armas":
                nombre, precio, cantidad = datos
                nombre_limpio = regex_color.sub('', nombre)

                if opcion_filtro in (0, 1):  # Nombre
                    datos_ordenados.append((nombre_limpio, nombre, precio, cantidad))
                elif opcion_filtro in (2, 3):  # Precio
                    datos_ordenados.append((precio, nombre, cantidad))
                elif opcion_filtro in (4, 5):  # Cantidad
                    datos_ordenados.append((cantidad, nombre, precio))

        if opcion_filtro % 2 == 1:  # impares son DESCENDENTES
            datos_ordenados.sort(reverse=True)
        else:
            datos_ordenados.sort()

        for datos in datos_ordenados:
            if tipo == "completo":
                if opcion_filtro in (0, 1):
                    nombre_limpio, nombre, precio, rareza, cantidad = datos
                elif opcion_filtro in (2, 3):
                    precio, nombre, rareza, cantidad = datos
                elif opcion_filtro in (4, 5):
                    orden, nombre, precio, rareza, cantidad = datos
                elif opcion_filtro in (6, 7):
                    cantidad, nombre, precio, rareza = datos
                print (nombre, "\t|", precio, "\t|", rareza, "\t|", cantidad)

            elif tipo == "camuflajes":
                if opcion_filtro in (0, 1):
                    nombre_limpio, nombre, precio, rareza, cantidad = datos
                elif opcion_filtro in (2, 3):
                    precio, nombre, rareza, cantidad = datos
                elif opcion_filtro in (4, 5):
                    orden, nombre, precio, rareza, cantidad = datos
                elif opcion_filtro in (6, 7):
                    cantidad, nombre, precio, rareza = datos
                print (nombre, "\t|", precio, "\t|", rareza, "\t|", cantidad)

            elif tipo == "armas":
                if opcion_filtro in (0, 1):
                    nombre_limpio, nombre, precio, cantidad = datos
                elif opcion_filtro in (2, 3):
                    precio, nombre, cantidad = datos
                elif opcion_filtro in (4, 5):
                    cantidad, nombre, precio = datos
                print (nombre, "\t|", precio, "\t|", cantidad)

        print("\n")
        for indice in range(len(opciones_filtros)):
            if indice == opcion_filtro:
                print("\033[92m> \033[0m" + opciones_filtros[indice])
            else:
                print("  " + opciones_filtros[indice])
        print("\nUse las flechas para cambiar filtros o ENTER para salir\n")
        print("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        if sys.platform.startswith("win"):
            tecla = _leer_tecla_windows()
            if tecla == '\xe0':
                tecla = _leer_tecla_windows()
                if tecla == 'H':
                    opcion_filtro = (opcion_filtro - 1) % len(opciones_filtros)
                elif tecla == 'P':
                    opcion_filtro = (opcion_filtro + 1) % len(opciones_filtros)
            elif tecla == '\r':
                menu_activo = False
        else:
            entrada = sys.stdin.fileno()
            configuracion_anterior = termios.tcgetattr(entrada)
            try:
                tty.setraw(entrada)
                tecla1 = sys.stdin.read(1)

                if tecla1 == '\x1b':
                    tecla2 = sys.stdin.read(1)
                    tecla3 = sys.stdin.read(1)
                    if tecla2 == '[':
                        if tecla3 == 'A':
                            opcion_filtro = (opcion_filtro - 1) % len(opciones_filtros)
                        elif tecla3 == 'B':
                            opcion_filtro = (opcion_filtro + 1) % len(opciones_filtros)
                    elif tecla2 == 'O' and tecla3 == 'M':
                        menu_activo = False
                elif tecla1 in ('\n', '\r'):
                    menu_activo = False
            finally:
                termios.tcsetattr(entrada, termios.TCSADRAIN, configuracion_anterior)

    return opcion_filtro

def mostrar_menu_enciclopedia(titulo, diccionario, opciones_filtros, tipo, regex_color=None, orden_rareza=None):
    opcion_filtro = 0
    menu_activo = True

    while menu_activo:
        os.system(limpiar)
        print("<<<<<<<<<<<<<<<<<<<<<< " + titulo + " >>>>>>>>>>>>>>>>>>>>>>>>")

        if tipo == "camuflajes":
            print("Nombre:", "\t| Precio:", "\t| Rareza:", "\t| Probabilidad:")
        elif tipo == "armas":
            print("Nombre:", "\t| Precio:", "\t| Probabilidad:")

        datos_ordenados = []

        for clave, datos in diccionario.items():
            if tipo == "camuflajes":
                nombre, rareza, precio, probabilidad = datos
                nombre_limpio = regex_color.sub('', nombre) if regex_color else nombre
                rareza_limpia = regex_color.sub('', rareza) if regex_color else rareza

                if opcion_filtro in (0, 1):  # Nombre
                    datos_ordenados.append((nombre_limpio, nombre, precio, rareza, probabilidad))
                elif opcion_filtro in (2, 3):  # Precio
                    datos_ordenados.append((precio, nombre, rareza, probabilidad))
                elif opcion_filtro in (4, 5):  # Rareza
                    indice_rareza = orden_rareza.index(rareza_limpia) if (orden_rareza and rareza_limpia in orden_rareza) else 0
                    datos_ordenados.append((indice_rareza, nombre, precio, rareza, probabilidad))
                elif opcion_filtro in (6, 7):  # Probabilidad
                    datos_ordenados.append((probabilidad, nombre, precio, rareza))

            elif tipo == "armas":
                nombre, precio, probabilidad = datos
                nombre_limpio = regex_color.sub('', nombre) if regex_color else nombre

                if opcion_filtro in (0, 1):  # Nombre
                    datos_ordenados.append((nombre_limpio, nombre, precio, probabilidad))
                elif opcion_filtro in (2, 3):  # Precio
                    datos_ordenados.append((precio, nombre, probabilidad))
                elif opcion_filtro in (4, 5):  # Probabilidad
                    datos_ordenados.append((probabilidad, nombre, precio))

        if opcion_filtro % 2 == 1:  # impares son DESC
            datos_ordenados.sort(reverse=True)
        else:
            datos_ordenados.sort()

        for datos in datos_ordenados:
            if tipo == "camuflajes":
                if opcion_filtro in (0, 1):
                    nombre_limpio, nombre, precio, rareza, probabilidad = datos
                elif opcion_filtro in (2, 3):
                    precio, nombre, rareza, probabilidad = datos
                elif opcion_filtro in (4, 5):
                    orden, nombre, precio, rareza, probabilidad = datos
                elif opcion_filtro in (6, 7):
                    probabilidad, nombre, precio, rareza = datos
                print(nombre, "\t|", precio, "\t|", rareza, "\t|", str(probabilidad * 100) + "%")

            elif tipo == "armas":
                if opcion_filtro in (0, 1):
                    nombre_limpio, nombre, precio, probabilidad = datos
                elif opcion_filtro in (2, 3):
                    precio, nombre, probabilidad = datos
                elif opcion_filtro in (4, 5):
                    probabilidad, nombre, precio = datos
                print(nombre, "\t|", precio, "\t|", str(probabilidad * 100) + "%")

        print("\n")
        for indice in range(len(opciones_filtros)):
            if indice == opcion_filtro:
                print("\033[92m> \033[0m" + opciones_filtros[indice])
            else:
                print("  " + opciones_filtros[indice])
        print("\nUse las flechas para cambiar filtros o ENTER para salir\n")
        print("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        if sys.platform.startswith("win"):
            tecla = _leer_tecla_windows()
            if tecla == '\xe0':
                tecla = _leer_tecla_windows()
                if tecla == 'H':
                    opcion_filtro = (opcion_filtro - 1) % len(opciones_filtros)
                elif tecla == 'P':
                    opcion_filtro = (opcion_filtro + 1) % len(opciones_filtros)
            elif tecla == '\r':
                menu_activo = False
        else:
            entrada = sys.stdin.fileno()
            configuracion_anterior = termios.tcgetattr(entrada)
            try:
                tty.setraw(entrada)
                tecla1 = sys.stdin.read(1)
                if tecla1 == '\x1b':
                    tecla2 = sys.stdin.read(1)
                    tecla3 = sys.stdin.read(1)
                    if tecla2 == '[':
                        if tecla3 == 'A':
                            opcion_filtro = (opcion_filtro - 1) % len(opciones_filtros)
                        elif tecla3 == 'B':
                            opcion_filtro = (opcion_filtro + 1) % len(opciones_filtros)
                    elif tecla2 == 'O' and tecla3 == 'M':
                        menu_activo = False
                elif tecla1 in ('\n', '\r'):
                    menu_activo = False
            finally:
                termios.tcsetattr(entrada, termios.TCSADRAIN, configuracion_anterior)

    return opcion_filtro

# CARGA DE DICCIONARIOS
def cargar_diccionario(nombre):
    try:
        with open("diccionarios/" + nombre + ".dat", "r") as archivo:
            return eval(archivo.read())
    except:
        return {}
# GUARDADO DE DICCIONARIOS
def guardar_diccionario(nombre, datos):
    try:
        with open("diccionarios/" + nombre + ".dat", "w") as archivo:
            archivo.write(repr(datos))
    except:
        print("ERROR: No se pudo guardar el diccionario", nombre)