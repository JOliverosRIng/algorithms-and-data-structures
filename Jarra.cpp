#include <iostream>
#include <thread>
#include <vector>
#include <random>
#include <chrono>
#include <mutex>
#include <string>
#include <algorithm>

using namespace std;
class Jarra {
private:
     int aguaDisponible;
     int capacidadMaxima;
     mutex mtx;

public:
     Jarra(int capacidad) : aguaDisponible(capacidad), capacidadMaxima(capacidad) {}
 
     void beber(int cantidad, const string& nombre) {
          lock_guard<mutex> lock(mtx);
          if (aguaDisponible >= cantidad) {
               cout << nombre << " está bebiendo " << cantidad << " ml de agua.\n";
               aguaDisponible -= cantidad;
               cout << "Agua restante: " << aguaDisponible << " ml\n\n";
          } else {
               cout << nombre << " quiso beber " << cantidad
                    << " ml, pero no hay suficiente agua.\n\n";
          }
     }

     void recargar(int cantidad, const string& nombre) {
          lock_guard<mutex> lock(mtx);

          int espacio = capacidadMaxima - aguaDisponible;
          int agregado = min(cantidad, espacio);
          aguaDisponible += agregado;

          cout << nombre << " recargó " << agregado << " ml de agua.\n";
          cout << "Agua disponible ahora: " << aguaDisponible << " ml\n\n";
     }
};

void persona(string nombre, Jarra& jarra) {
     random_device rd;
     mt19937 gen(rd());
     uniform_int_distribution<> consumo(100, 300);
     uniform_int_distribution<> espera(100, 1000);
     this_thread::sleep_for(chrono::milliseconds(espera(gen)));
     jarra.beber(consumo(gen), nombre);
}

void reabastecedor(string nombre, Jarra& jarra) {
     random_device rd;
     mt19937 gen(rd());
     uniform_int_distribution<> recarga(150, 400);
     uniform_int_distribution<> espera(500, 1500);

     for (int i = 0; i < 3; i++) {
          this_thread::sleep_for(chrono::milliseconds(espera(gen)));
          jarra.recargar(recarga(gen), nombre);
     }
}

int main() {
     Jarra jarra(1000);
     
     vector<thread> personas;
     for (int i = 1; i <= 5; i++) {
          personas.emplace_back(persona, "Persona-" + to_string(i), ref(jarra));
     }
     
     thread abastecedor(reabastecedor, "Reabastecedor", ref(jarra));
     
     for (auto& p : personas) {
          p.join();
     }
     
     abastecedor.join();
     
     return 0;
}