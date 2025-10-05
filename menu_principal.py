# -*- coding: utf-8 -*-


import utilidades
import runpy
import os


limpiar = "cls" if os.name == "nt" else "clear"

os.system(limpiar)
try:
    usuarios = utilidades.cargar_diccionario("usuarios")
    id_usuario_ingresado = utilidades.cargar_diccionario("sesion")
    nombre_usuario = usuarios[id_usuario_ingresado][0]
    sesion_iniciada = True
except:
    nombre_usuario = ""
    sesion_iniciada = False

opciones_menu = ["[0] Salir", "[1] Gestion de usuarios", "[2] Inventario", "[3] Apertura de cajas", "[4] Enciclopedia", "[5] Mercado", "[6] Modo Administrador"]


seleccion = utilidades.mostrar_menu("Menu Principal Dataskins", opciones_menu, sesion_iniciada, nombre_usuario)

if seleccion == 0:
    os.system(limpiar)
    print("\033[92mGracias por confiar en Dataskins!\033[0m\n")
    exit()
elif seleccion == 1:
    runpy.run_path("gestion_usuarios.py")
elif seleccion == 2:
    runpy.run_path("gestion_inventarios.py")
elif seleccion == 3:
    runpy.run_path("apertura_cajas.py")
elif seleccion == 4:
    runpy.run_path("enciclopedia.py")
elif seleccion == 5:
    runpy.run_path("gestion_mercado.py")
elif seleccion == 6:
    runpy.run_path("modo_admin.py")
