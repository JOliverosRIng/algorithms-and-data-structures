#include <iostream> // Librería para usar entrada y salida estándar

using namespace std;

int main() {
	//Declaracion de variables
   int numero1 = 0, numero2=0, mayor = 0, menor = 0, division = 0, residuo = 1;
   // Solicitud de variables
   cout << "VAMOS A TRABAJAR CON EL ALGORITMNO DE EUCLIDES REDUCIDO" << endl << "Ingrese el primer numero: " <<endl;
   cin >> numero1;
   cout << "Ingrese el segundo numero: " << endl;
   cin >> numero2;
   
   //Descubrir cual es el mayor de los dos
   if (numero1 > numero2) {
   	mayor = numero1;
   	menor = numero2;
   }else{
   	mayor = numero2;
   	menor = numero1;
   }
   
   //empezar la division entre los dos numeros
   while (residuo != 0 ){
   	division = mayor / menor;
   	residuo = mayor % menor;
   	mayor = menor;
  	menor = residuo;
   }
   
    cout << "El MCD es: " << mayor << endl; 
    
    return 0; // Indica que el programa terminó correctamente
}
