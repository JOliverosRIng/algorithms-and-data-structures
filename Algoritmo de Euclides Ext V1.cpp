#include <iostream>
using namespace std;

// Función para implementar el algoritmo de Euclides extendido
// Retorna el MCD de a y b, y los coeficientes x, y
int euclidesExtendido(int a, int b, int &x, int &y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    } else {
        int x1, y1;
        int mcd = euclidesExtendido(b, a % b, x1, y1);
        
        // Actualizamos los coeficientes x e y
        x = y1;
        y = x1 - (a / b) * y1;
        
        return mcd;
    }
}

int main() {
    int a, b;
    cout << "Ingresa dos números (a y b): ";
    cin >> a >> b;
    
    int x, y;
    int mcd = euclidesExtendido(a, b, x, y);
    
    cout << "MCD(" << a << ", " << b << ") = " << mcd << endl;
    cout << "Los coeficientes son: x = " << x << ", y = " << y << endl;
    cout << "Ecuación: " << a << " * " << x << " + " << b << " * " << y << " = " << mcd << endl;
    
    return 0;
}

