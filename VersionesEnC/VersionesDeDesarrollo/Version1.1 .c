#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define TAPE_SIZE 100

void binaryToDecimal(char *binary, int *decimal) {
    *decimal = 0;
    int base = 1; // 2^0

    // Recorremos el string binario de derecha a izquierda
    for (int i = strlen(binary) - 1; i >= 0; i--) {
        if (binary[i] == '1') {
            *decimal += base;
        }
        base *= 2; // Incrementamos la base
    }
}

void decimalToBinary(int decimal, char *binary) {
    int index = 0;
    if (decimal == 0) {
        binary[index++] = '0';
    } else {
        while (decimal > 0) {
            binary[index++] = (decimal % 2) + '0'; // Convertimos a carácter
            decimal /= 2;
        }
    }
    binary[index] = '\0';

    // Invertimos el string para tener el resultado correcto
    for (int i = 0; i < index / 2; i++) {
        char temp = binary[i];
        binary[i] = binary[index - 1 - i];
        binary[index - 1 - i] = temp;
    }
}

void addBinary(char *a, char *b, char *result) {
    int carry = 0;
    int i = strlen(a) - 1;
    int j = strlen(b) - 1;
    int k = 0;

    while (i >= 0 || j >= 0 || carry) {
        int sum = carry;
        if (i >= 0) sum += a[i--] - '0';
        if (j >= 0) sum += b[j--] - '0';
        result[k++] = (sum % 2) + '0'; // Guardamos el bit menos significativo
        carry = sum / 2; // Calculamos el nuevo carry
    }
    result[k] = '\0';

    // Invertimos el resultado para tener el orden correcto
    for (int m = 0; m < k / 2; m++) {
        char temp = result[m];
        result[m] = result[k - 1 - m];
        result[k - 1 - m] = temp;
    }
}

void subtractBinary(char *a, char *b, char *result) {
    int borrow = 0;
    int i = strlen(a) - 1;
    int j = strlen(b) - 1;
    int k = 0;

    while (i >= 0) {
        int sub = (a[i] - '0') - borrow;
        if (j >= 0) sub -= (b[j--] - '0');
        if (sub < 0) {
            sub += 2; // Tomamos prestado
            borrow = 1;
        } else {
            borrow = 0;
        }
        result[k++] = sub + '0'; // Guardamos el resultado
        i--;
    }
    result[k] = '\0';

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
    memmove(result, result + start, k - start + 1);
}

int main() {
    char binary1[TAPE_SIZE], binary2[TAPE_SIZE], result[TAPE_SIZE];
    int decimalResult;

    // Ejemplo de entrada: "101" (5 en decimal) y "011" (3 en decimal)
    printf("Ingresa el primer número binario: ");
    scanf("%s", binary1);
    printf("Ingresa el segundo número binario: ");
    scanf("%s", binary2);

    // Sumar
    addBinary(binary1, binary2, result);
    printf("Resultado de la suma: %s\n", result);
    binaryToDecimal(result, &decimalResult);
    printf("Resultado de la suma en decimal: %d\n", decimalResult);

    // Restar
    subtractBinary(binary1, binary2, result);
    printf("Resultado de la resta: %s\n", result);
    binaryToDecimal(result, &decimalResult);
    printf("Resultado de la resta en decimal: %d\n", decimalResult);

    return 0;
}
