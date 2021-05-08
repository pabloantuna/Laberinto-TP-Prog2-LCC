#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#define MAX_BUFFER 30


// getDimension: FILE* -> int
// esta funcion toma el archivo de entrada y devuelve la dimension
// del laberinto a generar
int getDimension(FILE *archivoEntrada){
    char buffer[MAX_BUFFER];
    int dimension;
    fscanf(archivoEntrada, "%[^\n]\n %d\n", buffer, &dimension);

    return dimension;
}

// getCantidadAleatorios: FILE* -> int
// esta funcion toma el archivo de entrada y devuelve la cantidad
// de obstaculos aleatorios del laberinto a generar
int getCantidadAleatorios(FILE *archivoEntrada){
    char buffer[MAX_BUFFER];
    // Leo primer linea
    fscanf(archivoEntrada, "%[^\n]\n", buffer);
    // Leo todos los obstaculos fijos
    while(fgetc(archivoEntrada) == '('){
        fscanf(archivoEntrada, "%[^\n]\n", buffer);
    }
    // Leo linea para saltearla
    fscanf(archivoEntrada, "%[^\n]\n", buffer);
    int cantidadAleatorios;
    // Leo cantidad de puntos aleatorios
    fscanf(archivoEntrada, "%d\n", &cantidadAleatorios);

    return cantidadAleatorios;
}

// leerPunto: FILE* -> char** -> int -> char -> char -> int
// esta funcion toma el archivo de entrada el laberinto, la dimension
// el caracter a escribir en el laberinto y el caracter con el cual comparar para saber si se puede escribir en ese lugar del laberinto
// devuelve un 1 que representa que pudo colocar el punto o un 0 que representa un error
int leerPunto(FILE *archivoEntrada, char **laberinto, int dimension, char charToUse, char caracterComparacion){
    int coordenadasX, coordenadasY, valido = 1;
    // Leo el punto
    fscanf(archivoEntrada, "%d,%d)\n", &coordenadasY, &coordenadasX);
    coordenadasX--;
    coordenadasY--;
    // Si el punto esta dentro del laberinto
    if(coordenadasY >= 0 && coordenadasY < dimension && coordenadasX >= 0 && coordenadasX < dimension){
        // Si el lugar en el laberinto esta disponible
        if(laberinto[coordenadasY][coordenadasX] == caracterComparacion){
            laberinto[coordenadasY][coordenadasX] = charToUse;
        } 
        else valido = 0;
    }
    else valido = 0;

    return valido;
}

// crearLaberinto: int -> char -> char**
// esta funcion toma la dimension y un char con el cual inicializar el laberinto
// devolviendo el laberinto inicializado con el caracter indicado
char **crearLaberinto(int dimension, char inicializador){
    char **laberinto = malloc(sizeof(char*) * dimension);
    int contador;
    // Asigno la memoria a cada puntero
    for(contador = 0; contador < dimension; contador++){
        laberinto[contador] = malloc(sizeof(char) * dimension + 1);
    }
    // Inicializo la primer fila del laberinto
    for(contador = 0; contador < dimension; contador++){
        laberinto[0][contador] = inicializador;
    }
    laberinto[0][dimension] = '\0';
    // Copio la fila inicializada al resto de filas
    for(contador = 0; contador < dimension; contador++){
        strcpy(laberinto[contador], laberinto[0]);
    }
    return laberinto;
}

// generarPuntosAleatorios: int -> int -> char** -> char -> char
// esta funcion toma la dimension, la cantidad de numeros aleatorios, el laberinto, 
// el caracter a comparar para saber si el lugar esta disponible en el laberinto
// y el caracter a escribir en el laberinto
void generarPuntosAleatorios(int dimension, int cantidadAleatorios, char **laberinto, char caracterComparacion, char charToUse){
    int contador, done, coordenadasY, coordenadasX;
    for(contador = 0; contador < cantidadAleatorios; contador++){
        done = 0;
        while(done == 0){
            coordenadasY = rand()%dimension;
            coordenadasX = rand()%dimension;
            if(laberinto[coordenadasY][coordenadasX] == caracterComparacion){
                laberinto[coordenadasY][coordenadasX] = charToUse;
                done = 1;
            }
        }
    }
}

// cambiarPorUnos: char** -> int -> int
// esta funcion toma el laberinto, la dimension, la cantidad de obstaculos fijos
// y recorre el laberinto cambiando los caracteres 2 por el caracter 1
void cambiarPorUnos(char **laberinto, int dimension, int cantParedesFijas){
    int contador, contador2, cantidadCambiados = 0;
    for (contador = 0; contador < dimension && cantidadCambiados < cantParedesFijas; contador++){
        for (contador2 = 0; contador2 < dimension && cantidadCambiados < cantParedesFijas; contador2++){
            if(laberinto[contador][contador2] == '2') {
                laberinto[contador][contador2] = '1';
                cantidadCambiados++;
            }
        }
    }
}

// completarLaberinto -> FILE* -> int -> char** -> char -> int
// esta funcion toma el archivo de entrada, la dimension, el laberinto y un caracter con el cual
// comparar para saber si una posicion esta libre (el caracter es el que identifica la disponibilidad del espacio en el laberinto)
int completarLaberinto(FILE *archivoEntrada, int dimension, char **laberinto, char caracterComparacion){
    char buffer[MAX_BUFFER];
    int valido = 1, lugaresUsados = 0, cantParedesFijas = 0;
    // Leo primer linea
    fscanf(archivoEntrada, "%[^\n]\n", buffer);
    // Leo la dimension
    fscanf(archivoEntrada, "%[^\n]\n", buffer);
    // Leo el titulo de obstaculos fijos
    fscanf(archivoEntrada, "%[^\n]\n", buffer);
    // Leo todos los obstaculos fijos
    while(fgetc(archivoEntrada) == '(' && valido == 1){
        if (caracterComparacion == '0') valido = leerPunto(archivoEntrada, laberinto, dimension, '1', caracterComparacion);
        else valido = leerPunto(archivoEntrada, laberinto, dimension, '2', caracterComparacion);
        if (valido == 1) {
            lugaresUsados++;
            cantParedesFijas++;
        }
    }

    if (valido == 1){
        // Leo linea para saltearla
        fscanf(archivoEntrada, "%[^\n]\n", buffer);
        int cantidadAleatorios;
        // Leo cantidad de puntos aleatorios
        fscanf(archivoEntrada, "%d\n", &cantidadAleatorios);

        // Leo linea para saltearla
        fscanf(archivoEntrada, "%[^\n]\n", buffer);
        // Leo punto de inicio
        if(fgetc(archivoEntrada) == '('){
            valido = leerPunto(archivoEntrada, laberinto, dimension, 'I', caracterComparacion);
            if (valido == 1) lugaresUsados++;
        }

        if(valido == 1){
            // Leo linea para saltearla
            fscanf(archivoEntrada, "%[^\n]\n", buffer);
            // Leo posicion objetivo
            if(fgetc(archivoEntrada) == '('){
                valido = leerPunto(archivoEntrada, laberinto, dimension, 'X', caracterComparacion);
                if (valido == 1) lugaresUsados++;
            }

            if(valido == 1){
                
                if(cantidadAleatorios > (dimension*dimension) - lugaresUsados) valido = 0;
                else{
                    // Genero puntos randoms
                    if (caracterComparacion == '0') generarPuntosAleatorios(dimension, cantidadAleatorios, laberinto, caracterComparacion, '1');
                    else {
                        cantidadAleatorios = (dimension*dimension)-cantidadAleatorios;
                        generarPuntosAleatorios(dimension, cantidadAleatorios, laberinto, caracterComparacion, '0');
                        // En este caso la inicializacion fue con '1' asi se escribieron '2' como identificador
                        // de los obstaculos fijos, se usa la funcion cambiarPorUnos para reemplazarlos por '1'
                        cambiarPorUnos(laberinto, dimension, cantParedesFijas);
                    }
                }
            }
        }
    }

    return valido;
}

// escribirSalida: FILE* -> char** -> int
// esta funcion toma el archivo de salida el laberinto y la dimension del mismo
// escribe un mensaje de error si el laberinto no se pudo generar,
// en caso contrario escribe el laberinto generado en el archivo
void escribirSalida(FILE *archivoSalida, char **laberinto, int dimension){
    if(laberinto == NULL){
        fprintf(archivoSalida, "ERROR\n");
        printf("ERROR\n");
    } else{
        int contador;
        for (contador = 0; contador < dimension; contador++){
            fprintf(archivoSalida, "%s\n" ,laberinto[contador]);
        }
    }
}

// main
int main(int argc, char *argv[]) {
    if(argc != 4) {                             //Chequeo que se ingresen todos los argumentos (nombres de archivos)
        printf("ERROR! Ingrese nombre de: ARCHIVO ENTRADA, ARCHIVO DE SALIDA e INGRESE SEED RANDOM\n");
        return -1;
    }
    FILE *archivoEntrada = fopen(argv[1],"r");
    FILE *archivoSalida = fopen(argv[2],"w+");

    srand(atoi(argv[3]));
    int dimension = getDimension(archivoEntrada);

    char **laberinto;
    int cantAleatorios = getCantidadAleatorios(archivoEntrada), noValido = 0;
    rewind(archivoEntrada);
    char caracterComparacion;
    // Si la cantidad de aleatorios que quiero generar es mayor a la mitad del laberinto
    if (cantAleatorios > (dimension*dimension)/2){
        // Inicialiazo el laberinto con '1' para luego ubicar '0' en lugar de '1' como 
        // randoms, de esta forma se generan menos random
        caracterComparacion = '1';
        laberinto = crearLaberinto(dimension, caracterComparacion);
    } 
    else {
        caracterComparacion = '0';
        laberinto = crearLaberinto(dimension, caracterComparacion);
    }

    // Si hubo algun error al intentar completar el laberinto
    if(completarLaberinto(archivoEntrada, dimension, laberinto, caracterComparacion) == 0){
        int contador;
        // Libero la memoria
        for (contador = 0; contador < dimension; contador++){
            free(laberinto[contador]);
        }
        free(laberinto);
        // seteo laberinto a NULL
        laberinto = NULL;
        noValido = 1;
    }

    escribirSalida(archivoSalida, laberinto, dimension);

    // Si el laberinto no es NULL (no libere memoria) libero la memoria    
    if(laberinto != NULL){
        int contador;
        for (contador = 0; contador < dimension; contador++){
            free(laberinto[contador]);
        }
        free(laberinto);
        laberinto = NULL;
    }

    // Cierro archivos
    fclose(archivoEntrada);
    fclose(archivoSalida);

    return noValido;
}