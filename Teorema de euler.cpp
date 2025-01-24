#include <iostream>
using namespace std;

// Function to calculate the greatest common divisor (GCD)
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Function to calculate Euler's Totient function f(n)
int eulerTotient(int n) {
    int result = n;  // Start with result = n
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {  // If i is a divisor of n
            while (n % i == 0) {
                n /= i;
            }
            result -= result / i;  // Apply the totient formula
        }
    }
    if (n > 1) {
        result -= result / n;  // Handle the last prime factor
    }
    return result;
}

// Function to compute (a^b) % n using binary exponentiation
int modExponentiation(int a, int b, int n) {
    int result = 1;
    a = a % n;  // In case a is larger than n
    while (b > 0) {
        if (b % 2 == 1) {  // If b is odd, multiply result by a
            result = (result * a) % n;
        }
        a = (a * a) % n;  // Square the base
        b /= 2;  // Divide the exponent by 2
    }
    return result;
}

int main() {
    int a, n;

    // Input values for a and n
    cout << "Enter a number a: ";
    cin >> a;
    cout << "Enter a number n: ";
    cin >> n;

    // Check if a and n are coprime (GCD(a, n) should be 1)
    if (gcd(a, n) != 1) {
        cout << "a and n are not coprime. Euler's theorem cannot be applied." << endl;
        return 0;
    }

    // Calculate Euler's Totient function f(n)
    int phi_n = eulerTotient(n);

    // Apply Euler's Theorem: a^f(n) = 1 (mod n)
    int result = modExponentiation(a, phi_n, n);

    cout << "According to Euler's Theorem: " << a << "^" << phi_n << " mod " << n << " = " << result << endl;
    
    return 0;
}

