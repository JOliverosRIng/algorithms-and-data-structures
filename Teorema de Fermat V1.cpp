#include <iostream>
using namespace std;

// Funci�n para verificar si un n�mero es primo
bool esPrimo(int p) {
    if (p <= 1) return false; 
    for (int i = 2; i * i <= p; i++) { 
        if (p % i == 0) return false; 
    }
    return true;
}

// Funci�n para verificar si un n�mero es natural
bool esNatural(int a) {
    return a >= 1; 
}

// Funci�n para calcular (a^(p-1)) % p usando exponenciaci�n modular
int modExponentiation(int a, int exp, int p) {
    long long result = 1;
    long long base = a % p;

    while (exp > 0) {
        if (exp % 2 == 1) { 
            result = (result * base) % p;
        }
        base = (base * base) % p;
        exp /= 2;
    }

    return result % p;
}

int main() {
    int a, p;

    // Entrada de datos
    cout << "Ingrese un n�mero primo (p): ";
    cin >> p;

    // Validar si p es primo
    if (!esPrimo(p)) {
        cout << "El n�mero ingresado no es primo." << endl;
        return 0;
    }

    cout << "Ingrese un n�mero natural (a) que no sea divisible por " << p << ": ";
    cin >> a;

    // Validar si a es natural
    if (!esNatural(a)) {
        cout << "El n�mero ingresado no es natural." << endl;
        return 0;
    }

    // Validar si a no es divisible por p
    if (a % p == 0) {
        cout << "El n�mero 'a' no debe ser divisible por 'p'." << endl;
        return 0;
    }

    // Aplicar el peque�o teorema de Fermat
    int resultado = modExponentiation(a, p - 1, p);

    // Verificar si (a^(p-1)) % p == 1
    if (resultado == 1) {
        cout << "El peque�o teorema de Fermat se cumple: " << a << "^" << p - 1
             << " mod " << p << " = 1" << endl;
    } else {
        cout << "El peque�o teorema de Fermat no se cumple." << endl;
    }

    return 0;
}

