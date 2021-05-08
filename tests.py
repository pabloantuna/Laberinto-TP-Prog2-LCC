from SolucionadorLaberinto import *

# Hay 2 archivos para este test, uno que contiene el laberinto
# como matriz tal como lo devuelve el programa en C
# otro que contiene el resultado del laberinto como lista (es decir como lo va a trabajar el programa en python) en la primer linea
# y los puntos de partida y llegada que deberia devolver la funcion leerArchivo en la segunda linea
def test_leerArchivo():
    laberinto = []
    archivoEntrada = open("entradaTestLeerArchivo.txt", "r")
    respuesta = leerArchivo(archivoEntrada, laberinto)
    archivoSalida = open("salidaTestLeerArchivo.txt", "r")
    assert(eval(archivoSalida.readline()) == laberinto)
    assert(eval(archivoSalida.readline()) == respuesta)
    laberinto = []
    archivoEntrada.close()
    archivoSalida.close()

# Hay 1 archivo para este test, que contiene la cantidad de tests (laberintos a testear) en la primer linea
# luego 3 lineas por cada laberinto a testear que son
# la primera tiene al laberinto como lista de strings
# la segunda los puntos de partida y llegada como tupla de tuplas
# y la tercera el diccionario de padres que deberia devolver la funcion recorrerMatriz
def test_recorrerMatriz():
    archivoEntrada = open("entradaTestRecorrerMatriz.txt", "r")
    cantidadTests = eval(archivoEntrada.readline())
    contador = 0
    while contador < cantidadTests:
        laberinto = eval(archivoEntrada.readline())
        puntos = eval(archivoEntrada.readline())
        padres = recorrerMatriz(laberinto, puntos[0], puntos[1])
        assert(eval(archivoEntrada.readline()) == padres)
        contador += 1
    archivoEntrada.close()

# Hay 1 archivo para este test, el cual contiene
# una linea que contiene la cantidad de laberintos que se usaran en el test
# luego 3 lineas por laberinto siendo una para el laberinto ya como lista de strings
# otra para los puntos de partida y llegada ya como tupla de tuplas
# y la tercera el camino que deberia obtenerse
def test_getCamino():
    archivoEntrada = open("entradaTestGetCamino.txt", "r")
    cantLaberintos = eval(archivoEntrada.readline())
    contador = 0
    while (contador < cantLaberintos):
        laberinto = eval(archivoEntrada.readline())
        puntos = eval(archivoEntrada.readline())
        camino = getCamino(puntos[0], puntos[1], laberinto)
        assert(eval(archivoEntrada.readline()) == camino)
        contador += 1
    archivoEntrada.close()

# Hay 1 archivo para este test, el cual contiene
# la cantidad de tests a probar (cantidad de laberintos a testear) en la primer linea
# luego por cada uno de esos tests hay 6 lineas que indican 
# la primera el laberinto a testear ya como lista de string
# la segunda los puntos de partida y llegada del laberindo ya como tupla de tuplas
# luego 4 lineas que contienen un 1 o un 0 cada una que representan si
# se desplaza o no hacia derecha, izquierda, arriba, abajo (respectivamente)
# luego n lineas (siendo n la cantidad de 1s usados) que tienen un valor booleano
# que representa si al desplazarse a cada una de las direcciones llega o no
# al punto de llegada (True = llega, False = no llega)
# (cada valor booleano esta relacionado con uno de los '1's colocados anteriormente y se relacionan en el orden escrito, 
# es decir, el primer valor booleano representa la respuesta del primer 1 colocado y asi sucesivamente)
def test_checkearPunto():
    archivoEntrada = open("entradaTestCheckearPuntos.txt", "r")
    cantidadTests = eval(archivoEntrada.readline())
    contador = 0
    while contador < cantidadTests:
        laberinto = eval(archivoEntrada.readline())
        puntos = eval(archivoEntrada.readline())
        derecha = eval(archivoEntrada.readline())
        izquierda = eval(archivoEntrada.readline())
        arriba = eval(archivoEntrada.readline())
        abajo = eval(archivoEntrada.readline())
        padres = {(puntos[0]): []}
        cola = []

        if(derecha == 1):
            esLlegada = checkearPunto(padres,laberinto,cola,puntos[0],puntos[1],1,0)
            assert(esLlegada == eval(archivoEntrada.readline()))
        if(izquierda == 1):
            esLlegada = checkearPunto(padres,laberinto,cola,puntos[0],puntos[1],-1,0)
            assert(esLlegada == eval(archivoEntrada.readline()))
        if(arriba == 1):
            esLlegada = checkearPunto(padres,laberinto,cola,puntos[0],puntos[1],0,1)
            assert(esLlegada == eval(archivoEntrada.readline()))
        if(abajo == 1):
            esLlegada = checkearPunto(padres,laberinto,cola,puntos[0],puntos[1],0,-1)
            assert(esLlegada == eval(archivoEntrada.readline()))
        contador += 1

    archivoEntrada.close()
