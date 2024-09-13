#include <stdio.h>   // Biblioteca para operaciones de entrada y salida estándar
#include <string.h>  // Biblioteca para manipulación de strings
#include <stdlib.h>  // Biblioteca para funciones de memoria dinámica y otras utilidades

#define TAPE_SIZE 100  // Definimos un tamaño máximo para los strings binarios

// Función para convertir un número binario (string) a decimal (entero)
void binaryToDecimal(char *binary, int *decimal) {
    *decimal = 0;  // Inicializamos el resultado decimal
    int base = 1;  // Base para binario (2^0)

    // Recorremos el string binario de derecha a izquierda
    for (int i = strlen(binary) - 1; i >= 0; i--) {
        if (binary[i] == '1') {  // Si el bit es 1, sumamos el valor correspondiente
            *decimal += base;
        }
        base *= 2;  // Incrementamos la base (2^1, 2^2, ...)
    }
}

// Función para convertir un número decimal (entero) a binario (string)
void decimalToBinary(int decimal, char *binary) {
    int index = 0;  // Índice para construir el string binario
    if (decimal == 0) {  // Caso especial para el número 0
        binary[index++] = '0';
    } else {
        while (decimal > 0) {  // Mientras el decimal sea mayor a 0
            binary[index++] = (decimal % 2) + '0';  // Convertimos a carácter y guardamos el bit
            decimal /= 2;  // Reducimos el decimal dividiéndolo por 2
        }
    }
    binary[index] = '\0';  // Terminamos el string

    // Invertimos el string para obtener el resultado correcto
    for (int i = 0; i < index / 2; i++) {
        char temp = binary[i];
        binary[i] = binary[index - 1 - i];
        binary[index - 1 - i] = temp;
    }
}

// Función para sumar dos números binarios
void addBinary(char *a, char *b, char *result) {
    int carry = 0;  // Variable de acarreo
    int i = strlen(a) - 1;  // Índice para el primer número binario
    int j = strlen(b) - 1;  // Índice para el segundo número binario
    int k = 0;  // Índice para el resultado

    // Mientras haya bits que procesar o haya acarreo
    while (i >= 0 || j >= 0 || carry) {
        int sum = carry;  // Comenzamos con el acarreo
        if (i >= 0) sum += a[i--] - '0';  // Sumamos bit de a si existe
        if (j >= 0) sum += b[j--] - '0';  // Sumamos bit de b si existe
        result[k++] = (sum % 2) + '0';  // Guardamos el bit menos significativo en el resultado
        carry = sum / 2;  // Calculamos el nuevo acarreo
    }
    result[k] = '\0';  // Terminamos el string

    // Invertimos el resultado para tener el orden correcto
    for (int m = 0; m < k / 2; m++) {
        char temp = result[m];
        result[m] = result[k - 1 - m];
        result[k - 1 - m] = temp;
    }
}

// Función para restar dos números binarios
void subtractBinary(char *a, char *b, char *result) {
    int borrow = 0;  // Variable de préstamo
    int i = strlen(a) - 1;  // Índice para el primer número binario
    int j = strlen(b) - 1;  // Índice para el segundo número binario
    int k = 0;  // Índice para el resultado

    // Mientras haya bits que procesar
    while (i >= 0) {
        int sub = (a[i] - '0') - borrow;  // Realizamos la resta considerando el préstamo
        if (j >= 0) sub -= (b[j--] - '0');  // Restamos bit de b si existe
        if (sub < 0) {  // Si el resultado es negativo, tomamos prestado
            sub += 2;
            borrow = 1;
        } else {
            borrow = 0;
        }
        result[k++] = sub + '0';  // Guardamos el resultado
        i--;
    }
    result[k] = '\0';  // Terminamos el string

    // Invertimos el resultado para tener el orden correcto
    for (int m = 0; m < k / 2; m++) {
        char temp = result[m];
        result[m] = result[k - 1 - m];
        result[k - 1 - m] = temp;
    }

    // Eliminamos ceros a la izquierda
    int start = 0;
    while (result[start] == '0' && start < k - 1) {
        start++;
    }
    memmove(result, result + start, k - start + 1);  // Movemos el resultado hacia el inicio del array
}

int main() {
    char binary1[TAPE_SIZE], binary2[TAPE_SIZE], result[TAPE_SIZE];  // Variables para los números binarios y el resultado
    int decimalResult;  // Variable para almacenar el resultado en decimal

    // Solicitamos al usuario que ingrese dos números binarios
    printf("Ingresa el primer número binario: ");
    scanf("%s", binary1);
    printf("Ingresa el segundo número binario: ");
    scanf("%s", binary2);

    // Sumar los dos números binarios
    addBinary(binary1, binary2, result);
    printf("Resultado de la suma: %s\n", result);
    binaryToDecimal(result, &decimalResult);  // Convertimos el resultado a decimal
    printf("Resultado de la suma en decimal: %d\n", decimalResult);

    // Restar los dos números binarios
    subtractBinary(binary1, binary2, result);
    printf("Resultado de la resta: %s\n", result);
    binaryToDecimal(result, &decimalResult);  // Convertimos el resultado a decimal
    printf("Resultado de la resta en decimal: %d\n", decimalResult);

    return 0;  // Fin del programa
}
