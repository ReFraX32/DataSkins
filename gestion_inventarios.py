# -*- coding : utf-8 -*-


import utilidades
import os
import re
import runpy

limpiar = "cls" if os.name == "nt" else "clear"
os.system(limpiar)

try:
    armas = utilidades.cargar_diccionario("armas")
    camuflajes = utilidades.cargar_diccionario("camuflajes")
    inventarios = utilidades.cargar_diccionario("inventarios")
except:
    print("ERROR: Los diccionarios no existen")
    exit()

try:
    usuarios = utilidades.cargar_diccionario("usuarios")
    id_usuario_ingresado = utilidades.cargar_diccionario("sesion")
    nombre_usuario_ingresado = usuarios[id_usuario_ingresado][0]
except:
    print("ERROR: No hay sesion iniciada")
    input("Presione ENTER para ir a la gestion de usuarios")
    runpy.run_path("gestion_usuarios.py")

regex_color = re.compile(r'\033\[[0-9;]*m')
orden_rareza = ("COMUN", "POCO COMUN", "RARO", "EPICO", "MITICO", "LEGENDARIO")

os.system(limpiar)

inventario_completo = {}
inventario_armas = {}
inventario_camuflajes = {}

for claves, cantidad in inventarios.items():
    id_usuario, id_camuflaje, id_arma = claves
    if id_usuario_ingresado == id_usuario:
        nombre_camuflaje, rareza, precio_camuflaje, probabilidad_camuflaje = camuflajes[id_camuflaje]
        nombre_arma, precio_arma, probabilidad_arma = armas[id_arma]
        nombre_completo = nombre_arma + " " + nombre_camuflaje
        precio_final = precio_arma + precio_camuflaje
        inventario_completo[(id_camuflaje, id_arma)] = [nombre_completo, precio_final, rareza, cantidad]

        if id_camuflaje in inventario_camuflajes:
            inventario_camuflajes[id_camuflaje][3] += 1
        else:
            inventario_camuflajes[id_camuflaje] = [nombre_camuflaje, precio_camuflaje, rareza, 1]

        if id_arma in inventario_armas:
            inventario_armas[id_arma][2] += 1
        else:
            inventario_armas[id_arma] = [nombre_arma, precio_arma, 1]

opciones_menu = ["[0] Volver al menu principal", "[1] Ver inventario completo", "[2] Ver inventario de solo camuflajes", "[3] Ver inventario de solo armas"]

while True:
    opcion_general = utilidades.mostrar_menu("Inventario de " + nombre_usuario_ingresado, opciones_menu)

    os.system(limpiar)

    if opcion_general == 0:
        runpy.run_path("menu_principal.py")

    elif opcion_general == 1:
        utilidades.mostrar_menu_filtrado(
            "Inventario COMPLETO de " + nombre_usuario_ingresado,
            inventario_completo,
            [
                "[0] Nombre ASCENDENTE", "[1] Nombre DESCENDENTE",
                "[2] Precio ASCENDENTE", "[3] Precio DESCENDENTE",
                "[4] Rareza ASCENDENTE", "[5] Rareza DESCENDENTE",
                "[6] Cantidad ASCENDENTE", "[7] Cantidad DESCENDENTE"
            ],
            "completo",
            regex_color,
            orden_rareza
        )

    elif opcion_general == 2:
        utilidades.mostrar_menu_filtrado(
            "Inventario de CAMUFLAJES de " + nombre_usuario_ingresado,
            inventario_camuflajes,
            [
                "[0] Nombre ASCENDENTE", "[1] Nombre DESCENDENTE",
                "[2] Precio ASCENDENTE", "[3] Precio DESCENDENTE",
                "[4] Rareza ASCENDENTE", "[5] Rareza DESCENDENTE",
                "[6] Cantidad ASCENDENTE", "[7] Cantidad DESCENDENTE"
            ],
            "camuflajes",
            regex_color,
            orden_rareza
        )

    elif opcion_general == 3:
        utilidades.mostrar_menu_filtrado(
            "Inventario de ARMAS de " + nombre_usuario_ingresado,
            inventario_armas,
            [
                "[0] Nombre ASCENDENTE", "[1] Nombre DESCENDENTE",
                "[2] Precio ASCENDENTE", "[3] Precio DESCENDENTE",
                "[4] Cantidad ASCENDENTE", "[5] Cantidad DESCENDENTE"
            ],
            "armas",
            regex_color
        )