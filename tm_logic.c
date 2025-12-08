/*
 * Turing Machine Simulation for L = {0^n 1^n | n >= 1}
 * Author: [Tu Nombre/Gemini]
 * Formal Definition:
 * Q = {q0, q1, q2, q3, q4}
 * Sigma = {0, 1}
 * Gamma = {0, 1, X, Y, B}
 * F = {q4}
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 1005 // 1000 chars + buffer
#define BLANK 'B'

// Estados definidos formalmente
typedef enum { q0, q1, q2, q3, q4, REJECT } State;

// Función para imprimir la Descripción Instantánea (ID) en archivo
// Formato: ... cinta_izquierda [estado] simbolo_actual ...
void print_id(FILE *f, char *tape, int head, State state) {
    // Encontrar limites visuales para no imprimir infinitos Blancos
    int min_print = 0;
    int max_print = strlen(tape);
    
    // Imprimir contenido relevante
    for (int i = min_print; i < max_print; i++) {
        if (i == head) {
            fprintf(f, " q%d ", state);
        }
        fprintf(f, "%c", tape[i]);
    }
    // Caso borde: si la cabeza está al final (en un B nuevo)
    if (head >= max_print) {
         fprintf(f, " q%d %c", state, BLANK);
    }
    fprintf(f, "\n");
}

int main() {
    char tape[MAX_LEN];
    char input[1001];
    int head = 0;
    State current_state = q0;
    FILE *file = fopen("traza_tm.txt", "w");

    if (file == NULL) {
        perror("Error abriendo archivo");
        return 1;
    }

    // 1. Entrada del usuario
    printf("--- Simulador Maquina de Turing (C Logic) ---\n");
    printf("Ingrese la cadena (max 1000 caracteres, ej: 0011): ");
    scanf("%1000s", input);

    // Inicializar cinta: Copiar input y llenar el resto con Blancos
    memset(tape, BLANK, MAX_LEN);
    strncpy(tape, input, strlen(input));
    tape[MAX_LEN - 1] = '\0'; // Null terminator por seguridad

    fprintf(file, "Traza de ejecucion para entrada: %s\n", input);
    fprintf(file, "Formato ID: alpha q_i beta (cabeza lee el primer char de beta)\n\n");

    // Ciclo de la maquina
    int steps = 0;
    while (current_state != q4 && current_state != REJECT && steps < 10000) {
        print_id(file, tape, head, current_state);
        
        char symbol = tape[head];
        
        // Lógica de Transición Delta (Basada en la imagen)
        switch (current_state) {
            case q0:
                if (symbol == '0') {
                    tape[head] = 'X'; // (q1, X, R)
                    current_state = q1;
                    head++;
                } else if (symbol == 'Y') {
                    tape[head] = 'Y'; // (q3, Y, R) - No cambia símbolo
                    current_state = q3;
                    head++;
                } else {
                    current_state = REJECT;
                }
                break;

            case q1:
                if (symbol == '0') {
                    // (q1, 0, R)
                    current_state = q1;
                    head++;
                } else if (symbol == '1') {
                    tape[head] = 'Y'; // (q2, Y, L)
                    current_state = q2;
                    head--;
                } else if (symbol == 'Y') {
                    // (q1, Y, R)
                    current_state = q1;
                    head++;
                } else {
                    current_state = REJECT;
                }
                break;

            case q2:
                if (symbol == '0') {
                    // (q2, 0, L)
                    current_state = q2;
                    head--;
                } else if (symbol == 'X') {
                    // (q0, X, R)
                    current_state = q0;
                    head++;
                } else if (symbol == 'Y') {
                    // (q2, Y, L)
                    current_state = q2;
                    head--;
                } else {
                    current_state = REJECT;
                }
                break;
            
            case q3:
                if (symbol == 'Y') {
                    // (q3, Y, R)
                    current_state = q3;
                    head++;
                } else if (symbol == BLANK) {
                    // (q4, B, R) -> Aceptación
                    current_state = q4;
                    head++; 
                } else {
                    current_state = REJECT;
                }
                break;

            default:
                current_state = REJECT;
                break;
        }
        steps++;
    }

    // Resultado final
    if (current_state == q4) {
        print_id(file, tape, head, current_state);
        fprintf(file, "\nRESULTADO: CADENA ACEPTADA\n");
        printf("Simulacion completa. Resultado: ACEPTADA. Ver traza_tm.txt\n");
    } else {
        fprintf(file, "\nRESULTADO: CADENA RECHAZADA (En estado q%d)\n", current_state);
        printf("Simulacion completa. Resultado: RECHAZADA. Ver traza_tm.txt\n");
    }

    fclose(file);
    return 0;
}