# -*- coding: utf-8 -*-


import os
import runpy

import utilidades

limpiar = "cls" if os.name == "nt" else "clear"

os.system(limpiar)
try:
    cajas = utilidades.cargar_diccionario("cajas")
    contenido_cajas = utilidades.cargar_diccionario("contenido_cajas")
    armas = utilidades.cargar_diccionario("armas")
    camuflajes = utilidades.cargar_diccionario("camuflajes")
    inventarios = utilidades.cargar_diccionario("inventarios")
    usuarios = utilidades.cargar_diccionario("usuarios")
except:
    print("No existen los archivos")
    exit()

opciones_menu = ["[0] Volver al menu", "[1] Editar cajas", "[2] Editar contenido de las cajas", "[3] Editar camuflajes", "[4] Editar armas", "[5] Editar usuarios"]

opcion_seleccionada = utilidades.mostrar_menu("Modo administrador", opciones_menu)


if opcion_seleccionada == 0:
    os.system(limpiar)
    print("\033[92mVolviendo al menu principal...\033[0m\n")
    runpy.run_path("menu_principal.py")
    exit()

if opcion_seleccionada == 1:
    sub_opciones_edicion_cajas_menu = ["[0] Volver al menu de Admin", "[1] Editar Nombre", "[2] Editar Detalle", "[3] Editar Precio"]
    sub_opciones_edicion_cajas = utilidades.mostrar_menu("Edicion de cajas", sub_opciones_edicion_cajas_menu)
    if sub_opciones_edicion_cajas == 0:
        os.system(limpiar)
        runpy.run_path("modo_admin.py")
    if sub_opciones_edicion_cajas == 1: #EDITAR NOMBRE
        while True:
            consulta_product = input("Ingresar Nombre De la Caja que quiere modificar: ")
            for id_caja, date_box in cajas.items():
                nombre_caja, detalle, precio = date_box
                if consulta_product == nombre_caja:
                    nombre_caja = input("Ingresar Nuevo Nombre: ")
                    cajas[id_caja] = [nombre_caja, detalle, precio]
                    utilidades.guardar_diccionario("cajas", cajas)
                    break
                else:
                    print("ERROR NO EXISTE EL PRODUCTO")
                    consulta_product = input("Ingresar UN NOMBRE VALIDO DE CAJA: ")
    elif sub_opciones_edicion_cajas == 2: #EDITAR DETALLE
        for id_caja, dato_box in cajas.items():
            nombre_caja, detalle, precio = cajas[id_caja]
        while True:
            consulta_product = input("Ingresar Nombre De la Caja que quiere modificar").capitalize()
            if consulta_product in nombre_caja:
                detalle = input("Ingresar Nuevo DETALLE: ")
                cajas[id_caja] = [nombre_caja, detalle, precio]
            else:
                print("ERROR NO EXISTE EL PRODUCTO")
                consulta_product = input("Ingresar UN NOMBRE VALIDO DE CAJA: ").capitalize()
    elif sub_opciones_edicion_cajas == 3:
        for id_caja, dato_box in cajas.items(): #EDITAR PRECIO
            nombre_caja, detalle, precio = cajas[id_caja]
        while True:
            consulta_product = input("Ingresar Nombre De la Caja que quiere modificar").capitalize()
            if consulta_product in nombre_caja:
                precio = input("Ingresar Nuevo PRECIO: ")
                cajas[id_caja] = [nombre_caja, detalle, precio]
            else:
                print("ERROR NO EXISTE EL PRODUCTO")
                consulta_product = input("Ingresar UN NOMBRE VALIDO DE CAJA: ")
elif opcion_seleccionada == 2: #EDITAR CONTENIDO DE LAS CAJAS
    for id_caja, date_box in cajas.items():
        nombre_caja, detalle, precio = cajas[id_caja]
        consulta_de_producto = input("Ingresar NOMBRE DE LA CAJA: ").capitalize()
        if consulta_de_producto in input:
            modificacion_cajas = input("Ingresar que quiere modificar en el contenido de cajas ARMAS O CAMUFLAJES: ").lower()
            if modificacion_cajas == "armas":
                nombre_arma = input("Ingresar Nueva Arma: ")
                for id_contenido, datos in contenido_cajas.items():
                    id_caja, id_arma, id_camuflaje = datos
                    nombre_arma, precio_arma, probabilidad_arma = armas[id_arma]
                    armas[id_arma] = [nombre_arma, precio_arma, probabilidad_arma]
            elif modificacion_cajas == "camuflajes":
                nombre_camuflaje = input("Ingresar Nuevo Camuflaje: ")
                for id_contenido, datos in contenido_cajas.items():
                    id_caja, id_arma, id_camuflaje = datos
                    nombre_camuflaje, rareza, precio_camuflaje, probabilidad_camuflaje = camuflajes[id_camuflaje]
                    camuflajes[id_camuflaje] = [nombre_camuflaje, rareza, precio_camuflaje, probabilidad_camuflaje]
elif opcion_seleccionada == 5:
    for id_usuario, datos in usuarios.items():
        nombre_usuario, correo, contrasenia, saldo = usuarios[id_usuario]
        