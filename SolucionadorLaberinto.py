### INICIO REPRESENTACION DE DATOS ###

# El laberinto es representado en este programa como una lista de strings

# Los puntos son representados como tuplas (y,x)

# Un camino es una lista de tuplas

# Tambien se utiliza un diccionario que tiene como keys a las tuplas y guarda dentro de cada key al 'padre' de cada key

### FIN REPRESENTACION DE DATOS ###
import sys
import subprocess
from random import * 

# Funcion que toma el archivo de entrada y una lista que representara el laberinto
# y devuelve una tupla de tuplas que contienen las coordenadas de la salida y del objetivo
def leerArchivo(archivo, laberinto):
    lineas = archivo.readlines()                                        # Leo las lineas del archivo
    numeroLinea = 0
    for linea in lineas:                                                # Recorro las lineas leidas
        if 'I' in linea:
            coordenadasSalida = numeroLinea, linea.index('I')           # Ubico las coordenadas del punto de partida
        if 'X' in linea:
            coordenadasLlegada = numeroLinea, linea.index('X')          # Ubico coordenadas del objetivo
        if(linea[-1] == '\n'):
            laberinto.append(linea[:-1])                                    # Guardo la linea leida sin el ultimo caracter ya que la entrada termina con un \n en cada linea
        else:
            laberinto.append(linea)
        numeroLinea += 1
    return coordenadasSalida, coordenadasLlegada

# Funcion que toma los padres, el laberinto, la "queue", el punto actual, el punto de llegada,
# un desplazamiento en coordenadas 'x' y un desplazamiento en coordenadas 'y'
# modifica la cola y agrega el punto como padre del punto a analizar si este nunca fue visitado
# devuelve un valor booleano que indica si el punto a analizar es el punto de llegada o no (true o false respectivamente)
def checkearPunto(padres, laberinto, cola, punto, puntoLlegada, desplazamientoX, desplazamientoY):
    puntoAnalizar = (punto[0]+desplazamientoY, punto[1]+desplazamientoX)
    if (puntoAnalizar not in padres.keys()):                 # si el punto a analizar nunca fue visitado
        padres[puntoAnalizar] = punto  # El padre de dicho punto es el punto actual
        cola.append((punto[0]+desplazamientoY, punto[1]+desplazamientoX))                   # agrego el punto a analizar a la lista que se utiliza como queue
    # Si el punto a analizar es el punto de llegada
    return (punto[0]+desplazamientoY == puntoLlegada[0] and punto[1]+desplazamientoX == puntoLlegada[1])

# Funcion basada en el algoritmo BFS que toma 
# el laberinto, un punto del cual comenzar a recorrer y un punto final hasta el cual recorrer
# Recorre la lista(laberinto) y devuelve los padres de los puntos analizados hasta encontrar
# el punto final o de todos los puntos que puede visitar si nunca pudo acceder al punto final
def recorrerMatriz(laberinto, puntoPartida, puntoLlegada):
    largoLaberinto = len(laberinto)         # la dimension del laberinto cuadrado
    topeSuperior = 0                        # minimo valor de la coordenada y
    topeInferior = largoLaberinto-1         # maximo valor de la coordenada y
    topeIzquierdo = topeSuperior            # minimo valor de la coordenada x
    topeDerecho = topeInferior              # maximo valor de la coordenada x

    encontrado = False

    padres = {}    

    # al primer punto ya le indico que no tiene padre
    padres[puntoPartida] = ()
    cola = []
    # el primer punto lo agrego a una lista que funcionara como queue
    # para la implementacion del algoritmo
    cola.append(puntoPartida)

    # mientras la queue no este vacia y no haya encontrado ya el puntoLlegada
    while cola != [] and not encontrado:
        # obtengo el primer elemento de la queue y lo elimino de la misma
        punto = cola.pop(0)
        
        # si es posible ir a la derecha en el laberinto
        if (punto[1]+1 <= topeDerecho):
            # si al ir a la derecha no hay un obstaculo
            if(laberinto[punto[0]][punto[1]+1] != '1'):
                encontrado = checkearPunto(padres,laberinto,cola,punto,puntoLlegada,1,0)

        # si es posible ir a la izquierda en el laberinto y no haya encontrado ya el puntoLlegada
        if (punto[1]-1 >= topeIzquierdo and not encontrado):
            # si al ir a la izquierda no hay un obstaculo
            if (laberinto[punto[0]][punto[1]-1] != '1'):
                encontrado = checkearPunto(padres,laberinto,cola,punto,puntoLlegada,-1,0)

        # si es posible ir arriba en el laberinto y no haya encontrado ya el puntoLlegada
        if (punto[0]-1 >= topeSuperior and not encontrado):
            # si al ir hacia arriba no hay un obstaculo
            if (laberinto[punto[0]-1][punto[1]] != '1'):
                encontrado = checkearPunto(padres,laberinto,cola,punto,puntoLlegada,0,-1)

        # si es posible ir hacia abajo en el laberinto y no haya encontrado ya el puntoLlegada
        if (punto[0]+1 <= topeInferior and not encontrado):
            # si al ir hacia abajo no hay un obstaculo
            if (laberinto[punto[0]+1][punto[1]] != '1'):
                encontrado = checkearPunto(padres,laberinto,cola,punto,puntoLlegada,0,1)

    return padres

# Funcion que toma un camino un archivo de salida y la posicion del objetivo
# y escribe el camino en el archivo de salida
def escribirSalida(camino, archivoSalida, puntoLlegada):
    # por cada tupla (punto) del camino
    for punto in camino:
        # escribo el punto en el archivo
        archivoSalida.write("(" + str(punto[0]+1) + "," + str(punto[1]+1) + ")")
        # si el punto no es el ultimo punto entonces agrego una coma
        if(punto != puntoLlegada):
            archivoSalida.write(",")

# Funcion que toma el punto de partida el punto de llegada y la lista que representa al laberinto
# y devuelve el camino que lleva desde el puntoPartida hasta el puntoLlegada o lista vacia si no hay camino
def getCamino(puntoPartida, puntoLlegada, laberinto):
    padres = recorrerMatriz(laberinto, puntoPartida, puntoLlegada)
    camino = []
    if (puntoLlegada in padres.keys()):
        camino.append(puntoLlegada)
        padreMio = padres[puntoLlegada]
        punto = padreMio
        camino.append(punto)
        while (padreMio != puntoPartida):
            padreMio = padres[punto]
            punto = padreMio
            camino.append(punto)
    
    camino.reverse()
    return camino    

def main():
    # Si paso la cantidad correcta de argumentos
    if(len(sys.argv) == 4):
        caminoObtenido = []
        error = False
        # Se guardan los nombres de los archivos que se pasan por terminal al ejecutar el programa
        nombreArchivoEntrada = sys.argv[1]
        nombreArchivoSalida = sys.argv[2]
        nombreArchivoEntradaC = sys.argv[3]
        # Mientras el camino obtenido al recorrer el laberinto sea lista vacia (esto es, no hay solucion)
        while caminoObtenido == [] and not error:
            # Ejecuto el programa hecho en C para crear el laberinto
            response = subprocess.run(["./a.out",nombreArchivoEntradaC, nombreArchivoEntrada, str(randint(0,1000000))])
            if (response.returncode == 0): 
                # Se abren los archivos con los nombres indicados
                archivoEntrada = open(nombreArchivoEntrada, "r")
                archivoSalida = open(nombreArchivoSalida, "w+")
                laberinto = []

                puntoPartida, puntoLlegada = leerArchivo(archivoEntrada, laberinto)
                # Cierro el archivo de entrada
                archivoEntrada.close()

                caminoObtenido = getCamino(puntoPartida, puntoLlegada, laberinto)
            else:
                error = True
                archivoSalida.write("ERROR! NO SE HA PASADO UN LABERINTO VALIDO")
        
        if(not error):
            # Una vez fuera del while, si no hubo error (es decir una vez que encontre solucion) escribo en el archivo de salida la respuesta
            escribirSalida(caminoObtenido, archivoSalida, puntoLlegada)

        # Cierro los archivos
        archivoEntrada.close()
        archivoSalida.close()
    else:
        print("Ingrese nombre de archivos: ENTRADA, SALIDA y ENTRADA DEL GENERADOR DE LABERINTOS")

if __name__ == "__main__":
    main()
