import random
import os

#Variables global del tablero
MINA = "*"
ESPACIO_SIN_ABRIR = "."
ESPACIO_ABIERTO = "-"
LETRAS = "ABCDEFGHI"
FILAS = len(LETRAS)
COLUMNAS = 9
BOMBAS = 10
tablero = []
minas = []
HA_GANADO = False
HA_PERDIDO = False
opcion = 1


def generar_minas(filas_cols, num_minas):
    """
    Función para generar el tablero con las minas
    """
    global minas
    minas = [True] * num_minas + [False] * (filas_cols **2 - num_minas)
    random.shuffle(minas)
    return [minas[i:i+filas_cols] for i in range(0, len(minas), filas_cols)]

def colocar_minas_en_tablero():
    global tablero
    global mina_matriz
    global FILAS
    global COLUMNAS

    mina_matriz = []
    filas = FILAS
    cols = COLUMNAS
    mina_matriz = [minas[i:i + cols] for i in range(0, len(minas), cols)]
    i = 0
    j = 0
    for i in range(FILAS):
        for j in range(COLUMNAS):
            if mina_matriz[i][j] == True:
                tablero[i][j] = MINA
    return


def inicializar_tablero():
    global tablero
    tablero = []
    """
    Rellena el tablero
    """
    for fila in range(FILAS):
        tablero.append([])
        for columna in range(COLUMNAS):
            tablero[fila].append(ESPACIO_SIN_ABRIR)
    return

def numero_a_letra(numero):
    """
    Convierte el número (comenzando en 0) a la letra
    """
    return LETRAS[numero]

def letra_a_numero(letra):
    """
    Devuelve el número que le corresponde a la letra COMENZANDO EN 0. Por ejemplo
    A: 0
    B: 1
    """
    numero = LETRAS.index(letra)
    return numero

def obtener_indices_a_partir_de_coordenadas(coordenadas):
    """
    Devuelve, a partir de una coordenada como A1, las coordenadas
    reales de la matriz; es decir, los índices. Por ejemplo, para
    A1 devolvería [0, 0]
    """
    letra = coordenadas[0:1]
    fila = letra_a_numero(letra)
    columna = int(coordenadas[1:3]) - 1
    return fila, columna


def imprimir_tablero():
    """
    Imprime el tablero, 
    lo convierte de matriz a algo entendible para el usuario
    """
    global FILAS
    global COLUMNAS
    print("")
    ultima_casilla = False
    # Imprimir esquina superior izquierda
    print("  ", end="")
    # Imprimir resto de encabezado
    for columna in range(COLUMNAS):
        print(str(columna + 1), end=" ")
    # Salto de línea
    print("")
    # Imprimir contenido...
    numero_fila = 0
    for fila in tablero:
        letra = numero_a_letra(numero_fila)
        print(letra, end=" ")
        for numero_columna, dato in enumerate(fila):
            # El tablero tiene los verdaderos datos, pero nosotros imprimimos otros para que el usuario no "descubra" lo que hay debajo
            verdadero_dato = ""
            if dato == MINA:
                if HA_GANADO or HA_PERDIDO:
                    verdadero_dato = MINA
                else:
                    verdadero_dato = ESPACIO_SIN_ABRIR
            elif dato == ESPACIO_ABIERTO:
                verdadero_dato = obtener_minas_cercanas(numero_fila, numero_columna)
            elif dato == ESPACIO_SIN_ABRIR:
                verdadero_dato = "."

            print(verdadero_dato, end=" ")
        print("")
        numero_fila += 1
    if HA_GANADO:
        print("GANASTE")
    elif HA_PERDIDO:
        print("PERDISTE")
    return

def generar_tablero():
    """
    Crea el tablero con las filas y columnas numeradas
    inicialmente pone todas las casillas con un punto
    """
    global tablero, FILAS, COLUMNAS
    tablero = []
    
    """
    Rellena el tablero
    """
    for fila in range(FILAS):
        tablero.append([])
        for columna in range(COLUMNAS):
            tablero[fila].append(ESPACIO_SIN_ABRIR)

    return

def abrir_casilla(coordenadas):
    global HA_GANADO, HA_PERDIDO, tablero
    fila, columna = obtener_indices_a_partir_de_coordenadas(coordenadas)
    # Qué había en la casilla?
    elemento_actual = tablero[fila][columna]
    # Si hay una mina, pierde y ya no se modifica nada
    if elemento_actual == MINA:
        HA_PERDIDO = True
        return
    # Si es un elemento sin abrir, lo abre
    if elemento_actual == ESPACIO_SIN_ABRIR:
        tablero[fila][columna] = ESPACIO_ABIERTO
    # Comprobamos si hay casillas sin abrir
    if no_hay_casillas_sin_abrir():
        HA_GANADO = True

def no_hay_casillas_sin_abrir():
    for fila in tablero:
        for columna in fila:
            if columna == ESPACIO_SIN_ABRIR:
                return False
    return True

def obtener_minas_cercanas(fila, columna):
    conteo = 0
    if fila <= 0:
        fila_inicio = 0
    else:
        fila_inicio = fila - 1
    if fila + 1 >= FILAS:
        fila_fin = FILAS - 1
    else:
        fila_fin = fila + 1

    if columna <= 0:
        columna_inicio = 0
    else:
        columna_inicio = columna - 1

    if columna + 1 >= COLUMNAS:
        columna_fin = COLUMNAS - 1
    else:
        columna_fin = columna + 1

    for f in range(fila_inicio, fila_fin + 1):
        for c in range(columna_inicio, columna_fin + 1):
            # Si es la central, la omitimos
            if f == fila and c == columna:
                continue
            if tablero[f][c] == MINA:
                conteo += 1
    return str(conteo)


def pedir_coordenada():
    """
    Pide una coordenada al usuario
    """
    print("Ingrese una coordenada valida (fila, columna) sin separacion: ")
    coordenada = int(input())
    return

def partida():
    """
    Mantiene el juego hasta que pierda o gane
    """

    return

def solicitar_casilla():
    global LETRAS, FILAS, COLUMNAS
    while True:
        casilla = input("Ingrese la casilla del tablero a abrir: ")
        casilla = casilla.upper()
        
        #if len(casilla) != 2 and len(casilla) != 3:
        #    print("Debes introducir una letra y un número")
        #    continue
        if not casilla[0].isalpha():
            print("El primer valor debe ser una letra")
            continue
        #if not casilla[1].isdigit():
        #    print("El segundo valor debe ser un número")
        #    continue
        if not casilla[0] in LETRAS:
            print("La letra debe estar en el rango " + LETRAS)
            continue
        if int(casilla[1]) <= 0 or int(casilla[1]) > COLUMNAS:
            print(f"El número debe estar en el rango 1-{COLUMNAS}")
            continue
        return casilla

def menu():
    """
    Opciones de inicio
    """
    print("\t== Bienvenido al juego del buscaminas ===")
    print("\t=========================================")
    print("")
    print("\tSelecciona un modo de juego:")
    print("\t1) Normal")
    print("\t2) Avanzado")
    print("\t3) Salir")
    print("")
    return

def ejecuta():
    global FILAS
    global COLUMNAS
    global BOMBAS
    global LETRAS

    if opcion == 1:
        LETRAS = "ABCDEFGHI"
        FILAS = len(LETRAS)
        COLUMNAS = 9
        BOMBAS = 10    
    else:
        if opcion == 2:
            LETRAS = "ABCDEFGHIJKLMNOP"
            FILAS = len(LETRAS)
            COLUMNAS = 16
            BOMBAS =25
    tablero = []
    minas = []
    inicializar_tablero()
    generar_tablero()
    generar_minas(FILAS, BOMBAS)
    colocar_minas_en_tablero()
    imprimir_tablero()
    while not HA_PERDIDO and not HA_GANADO:
        casilla = solicitar_casilla()
        abrir_casilla(casilla)
        imprimir_tablero()
    return 

#ejecución
opcion = 1
os.system("cls")
while True:
    menu() 
    opcion = int(input())
    if opcion == 1 or opcion == 2:
        ejecuta()
        input("El juego ha terminado...")
    if opcion == 3:
        break


