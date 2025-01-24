#include <iostream>
using namespace std;

// Función para verificar si un número es primo
bool esPrimo(int p) {
    if (p <= 1) return false; 
    for (int i = 2; i * i <= p; i++) { 
        if (p % i == 0) return false; 
    }
    return true;
}

// Función para verificar si un número es natural
bool esNatural(int a) {
    return a >= 1; 
}

// Función para calcular (a^(p-1)) % p usando exponenciación modular
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
    cout << "Ingrese un número primo (p): ";
    cin >> p;

    // Validar si p es primo
    if (!esPrimo(p)) {
        cout << "El número ingresado no es primo." << endl;
        return 0;
    }

    cout << "Ingrese un número natural (a) que no sea divisible por " << p << ": ";
    cin >> a;

    // Validar si a es natural
    if (!esNatural(a)) {
        cout << "El número ingresado no es natural." << endl;
        return 0;
    }

    // Validar si a no es divisible por p
    if (a % p == 0) {
        cout << "El número 'a' no debe ser divisible por 'p'." << endl;
        return 0;
    }

    // Aplicar el pequeño teorema de Fermat
    int resultado = modExponentiation(a, p - 1, p);

    // Verificar si (a^(p-1)) % p == 1
    if (resultado == 1) {
        cout << "El pequeño teorema de Fermat se cumple: " << a << "^" << p - 1
             << " mod " << p << " = 1" << endl;
    } else {
        cout << "El pequeño teorema de Fermat no se cumple." << endl;
    }

    return 0;
}

