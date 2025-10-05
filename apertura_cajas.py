# -*- coding: utf-8 -*-


import os
import time
import random
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
    print("ERROR: Los diccionarios no existen")
    exit()

resultados = []

try:
    id_usuario_ingresado = utilidades.cargar_diccionario("sesion")
except:
    print("ERROR: No hay sesion iniciada")
    input("Presione ENTER para ir a la gestion de usuarios")
    runpy.run_path("gestion_usuarios.py")

lista_cajas = []

for id_caja, datos in cajas.items():
    nombre_caja, detalle, precio = datos
    linea = nombre_caja + " | " + detalle + " | $" + str(precio)
    lista_cajas.append((id_caja, linea))

precio_caja_aleatoria = 5000.0

lista_cajas.append((-1, "\033[93mCaja Aleatoria | Contiene armas y camuflajes aleatorios | $" + str(precio_caja_aleatoria) + "\033[0m\n"))
lista_cajas.append((-2, "[Volver al menu principal]\n"))

indice_seleccionado = utilidades.mostrar_menu_cajas(
    "Apertura de cajas",
    lista_cajas
)

consulta_caja = lista_cajas[indice_seleccionado][0]

if consulta_caja == -2:
    runpy.run_path("menu_principal.py")
elif consulta_caja == -1:
    id_caja = -1

    cantidad_aleatoria = random.randint(5, 10)
    armas_aleatorias = random.sample(list(armas.keys()), cantidad_aleatoria)
    camuflajes_aleatorios = random.sample(list(camuflajes.keys()), cantidad_aleatoria)

    for i in range(cantidad_aleatoria):
        id_contenido = max(contenido_cajas.keys()) + 1
        id_arma = armas_aleatorias[i]
        id_camuflaje = camuflajes_aleatorios[i]
        contenido_cajas[id_contenido] = [id_caja, id_arma, id_camuflaje]

    consulta_caja = id_caja
    nombre_consulta_caja = "Caja Aleatoria"
    precio_caja = precio_caja_aleatoria
else:
    nombre_consulta_caja = cajas[consulta_caja][0]
    precio_caja = cajas[consulta_caja][2]

os.system(limpiar)

opciones_menu = ["[Regresar]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]", "[10]"]

cantidad_seleccionada = utilidades.mostrar_menu("Seleccione la cantidad que desea abrir de la " + nombre_consulta_caja, opciones_menu)

os.system(limpiar)

if cantidad_seleccionada == 0:
    runpy.run_path("apertura_cajas.py")

saldo = usuarios[id_usuario_ingresado][3]
precio_final = precio_caja * cantidad_seleccionada
resultante = saldo - precio_final

print("El precio final es de: $" + str(precio_final), "(Saldo disponible: $" + str(saldo) + ", resultante: " + str(resultante) + ")")
confirmacion = input("Ingrese 0 para regresar o cualquier otra tecla para continuar: ")
if confirmacion == "0":
    runpy.run_path("apertura_cajas.py")

contador = 0
armas_caja = []
camuflajes_caja = []

acumulador_probabilidad_armas = 0.0
acumulador_probabilidad_camuflajes = 0.0
contenido_filtrado = []

for id_contenido, datos in contenido_cajas.items():
    id_caja, id_arma, id_camuflaje = datos
    if id_caja == consulta_caja:
        contenido_filtrado.append(datos)
        nombre_arma, precio_arma, probabilidad_arma = armas[id_arma]
        nombre_camuflaje, rareza, precio_camuflaje, probabilidad_camuflaje = camuflajes[id_camuflaje]
        armas_caja.append(nombre_arma)
        camuflajes_caja.append(nombre_camuflaje)
        acumulador_probabilidad_armas += probabilidad_arma
        acumulador_probabilidad_camuflajes += probabilidad_camuflaje

if not armas_caja or not camuflajes_caja:
    print("ERROR: La caja seleccionada no tiene contenido disponible.")
    exit()

if saldo < precio_final:
    os.system(limpiar)
    faltante = precio_final - saldo
    print("Le falta $" + str(faltante) + " para realizar la compra, por favor recargue saldo")
    input("Presione ENTER para ser llevado a la gestion de usuarios")
    runpy.run_path("gestion_usuarios.py")
else:
    usuarios[id_usuario_ingresado][3] = resultante

while contador < cantidad_seleccionada:
    numero_aleatorio_armas = random.random() * acumulador_probabilidad_armas
    numero_aleatorio_camuflajes = random.random() * acumulador_probabilidad_camuflajes

    probabilidad_acumulada_armas = 0.0
    probabilidad_acumulada_camuflajes = 0.0

    id_arma_elegida = None
    nombre_arma_elegida = "???"
    id_camuflaje_elegido = None
    nombre_camuflaje_elegido = "???"

    for id_caja, id_arma, id_camuflaje in contenido_filtrado:
        nombre_arma, precio_arma, probabilidad_arma = armas[id_arma]
        nombre_camuflaje, rareza, precio_camuflaje, probabilidad_camuflaje = camuflajes[id_camuflaje]

        if id_arma_elegida is None:
            probabilidad_acumulada_armas += probabilidad_arma
            if numero_aleatorio_armas <= probabilidad_acumulada_armas:
                id_arma_elegida = id_arma
                nombre_arma_elegida = nombre_arma

        if id_camuflaje_elegido is None:
            probabilidad_acumulada_camuflajes += probabilidad_camuflaje
            if numero_aleatorio_camuflajes <= probabilidad_acumulada_camuflajes:
                id_camuflaje_elegido = id_camuflaje
                nombre_camuflaje_elegido = nombre_camuflaje

    resultado = nombre_arma_elegida + " " + nombre_camuflaje_elegido
    resultados.append(resultado)
    contador += 1

    clave = (id_usuario_ingresado, id_camuflaje_elegido, id_arma_elegida)
    if clave in inventarios:
        cantidad_objeto = inventarios[clave] + 1
    else:
        cantidad_objeto = 1
    inventarios[clave] = cantidad_objeto

utilidades.guardar_diccionario("usuarios", usuarios)

utilidades.guardar_diccionario("inventarios", inventarios)


for i in range(cantidad_seleccionada):
    os.system(limpiar)
    print(("\033[96mAbriendo caja..." + "[" + str(i + 1) + "/" + str(cantidad_seleccionada) + "]" + "\033[0m\n"))
    print("     _________________________")
    print("    /                      /|")
    print("   /                      / |")
    print("  /______________________/  |")
    print("  |______________________| /")
    time.sleep(1)

    os.system(limpiar)
    print(("\033[96mAbriendo caja..." + "[" + str(i + 1) + "/" + str(cantidad_seleccionada) + "]" + "\033[0m\n"))
    print("      ______________________")
    print("    /                     /  \\")
    print("   /_____________________/___\\")
    print("   \\                     \\   /")
    print("    \\_____________________\\_/")
    time.sleep(1)

    for j in range(30):
        os.system(limpiar)
        print("\033[96mAbriendo caja..." + "[" + str(i + 1) + "/" + str(cantidad_seleccionada) + "]" + "\033[0m\n")
        arma = armas_caja[j % len(armas_caja)]
        camuflaje = camuflajes_caja[j % len(camuflajes_caja)]
        print(">> Arma: " + arma)
        print(">> Camuflaje: " + camuflaje)
        tiempo = max(0.03, 0.15 - (cantidad_seleccionada * 0.01))
        time.sleep(tiempo)

    os.system(limpiar)
    print("\033[92mHas obtenido:\033[0m\n  > " + resultados[i])
    time.sleep(2)

if cantidad_seleccionada > 1:
    os.system(limpiar)
    print("Conseguiste:")
    for resultado in resultados:
        print("  > " + resultado)

input("\nPresione ENTER para volver al menu principal")
runpy.run_path("menu_principal.py")