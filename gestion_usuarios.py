# -*- coding: utf-8 -*-


import utilidades
import os
import runpy

limpiar = "cls" if os.name == "nt" else "clear"
os.system(limpiar)

try:
    usuarios = utilidades.cargar_diccionario("usuarios")
except:
    print("ERROR: Los diccionarios no existen")
    exit()

if len(usuarios) > 0:
    id_usuario = max(usuarios.keys()) + 1
else:
    id_usuario = 0

try:
    id_usuario_ingresado = utilidades.cargar_diccionario("sesion")
    nombre_usuario_ingresado = usuarios[id_usuario_ingresado][0]
    sesion_iniciada = True
except:
    nombre_usuario_ingresado = ""
    sesion_iniciada = False

opciones_menu = [
    "[0] Volver al menu principal",
    "[1] Registrarse",
    "[2] Iniciar sesion",
    "[3] Recargar saldo",
    "[4] Cerrar sesion"
]

while True:
    seleccion = utilidades.mostrar_menu("Gestion de usuarios", opciones_menu, sesion_iniciada, nombre_usuario_ingresado)

    if seleccion == 0:
        runpy.run_path("menu_principal.py")

    elif seleccion == 1:
        os.system(limpiar)
        print("Ingrese los datos solicitados: ")
        correo = input("\n\t\tCorreo electronico: ").lower()
        contrasenia = input("\n\t\t\tContrasenia: ")
        saldo = 0.0
        usuarios[id_usuario] = [nombre_usuario, correo, contrasenia, saldo]
        id_usuario += 1
        utilidades.guardar_diccionario("usuarios", usuarios)
        os.system(limpiar)
        print("Registro exitoso!, Por favor ahora inicie sesion.")
        input("Presione ENTER para continuar")

    elif seleccion == 2:
        os.system(limpiar)
        print("Ingrese los datos solicitados: ")
        correo_consulta = input("\n\tCorreo electronico: ").lower()
        contrasenia_consulta = input("\n\t\tContrasenia: ")
        os.system(limpiar)
        encontrado = False
        for id_temp, datos in usuarios.items():
            nombre_usuario, correo, contrasenia, saldo = datos
            if correo == correo_consulta and contrasenia == contrasenia_consulta:
                sesion_iniciada = True
                id_usuario_ingresado = id_temp
                nombre_usuario_ingresado = nombre_usuario

                utilidades.guardar_diccionario("sesion", id_usuario_ingresado)

                print("Sesion iniciada correctamente como: " + nombre_usuario)
                encontrado = True
                break
        if not encontrado:
            print("Correo o contrasenia incorrectos.")
        input("Presione ENTER para continuar")

    elif seleccion == 3:
        os.system(limpiar)
        if sesion_iniciada:
            print("Ingrese los datos solicitados: ")
            nro_tarjeta = input("\n\tTarjeta de credito/debito (16 digitos sin espacios): ")
            while len(nro_tarjeta) != 16 or not nro_tarjeta.isdigit():
                print("ERROR: Ingrese exactamente 16 digitos numericos.")
                nro_tarjeta = input("\n\tTarjeta de credito/debito (16 digitos sin espacios): ")

            recarga_saldo = input("\n\t\tSaldo a cargar: ")
            recarga_saldo = float(recarga_saldo)
            while recarga_saldo < 0:
                print("ERROR: Ingrese un numero mayor a 0")
                recarga_saldo = input("\n\t\tSaldo a cargar: ")
                recarga_saldo = float(recarga_saldo)
            usuarios[id_usuario_ingresado][3] += recarga_saldo
            utilidades.guardar_diccionario("usuarios", usuarios)
            os.system(limpiar)
            print("El pago se ha realizado correctamente!, su saldo ahora es de: $" + str(usuarios[id_usuario_ingresado][3]))
        else:
            print("Debe iniciar sesion primero.")
        input("Presione ENTER para continuar")

    elif seleccion == 4:
        os.system(limpiar)
        utilidades.guardar_diccionario("sesion", "")
        sesion_iniciada = False
        nombre_usuario_ingresado = ""
        input("Sesion cerrada exitosamente, presione ENTER para continuar")