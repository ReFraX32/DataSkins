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
except:
    print("ERROR: Los diccionarios no existen")
    exit()

regex_color = re.compile(r'\033\[[0-9;]*m')
orden_rareza = ("COMUN", "POCO COMUN", "RARO", "EPICO", "MITICO", "LEGENDARIO")

os.system(limpiar)

opciones_menu = ["[0] Volver al menu principal", "[1] Ver enciclopedia de camuflajes", "[2] Ver enciclopedia de armas"]

while True:
    opcion_general = utilidades.mostrar_menu("Enciclopedia", opciones_menu)

    os.system(limpiar)

    if opcion_general == 0:
        runpy.run_path("menu_principal.py")
        exit()
        break

    elif opcion_general == 1:
        utilidades.mostrar_menu_enciclopedia(
            "Enciclopedia de camuflajes",
            camuflajes,
            [
                "[0] Nombre ASCENDENTE", "[1] Nombre DESCENDENTE",
                "[2] Precio ASCENDENTE", "[3] Precio DESCENDENTE",
                "[4] Rareza ASCENDENTE", "[5] Rareza DESCENDENTE",
                "[6] Probabilidad ASCENDENTE", "[7] Probabilidad DESCENDENTE"
            ],
            "camuflajes",
            regex_color,
            orden_rareza
        )

    elif opcion_general == 2:
        utilidades.mostrar_menu_enciclopedia(
            "Enciclopedia de armas",
            armas,
            [
                "[0] Nombre ASCENDENTE", "[1] Nombre DESCENDENTE",
                "[2] Precio ASCENDENTE", "[3] Precio DESCENDENTE",
                "[4] Probabilidad ASCENDENTE", "[5] Probabilidad DESCENDENTE"
            ],
            "armas",
            regex_color
        )