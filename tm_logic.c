/* tm_logic.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 1005
#define BLANK 'B'

typedef enum { q0, q1, q2, q3, q4, REJECT } State;

void print_id(FILE *f, char *tape, int head, State state) {
    int max_print = strlen(tape);
    // Imprimimos un formato fácil de parsear para Python:
    // FORMATO: ESTADO|INDICE_CABEZA|CINTA_COMPLETA
    fprintf(f, "%d|%d|%s\n", state, head, tape);
}

int main(int argc, char *argv[]) {
    char tape[MAX_LEN];
    char input[1001];
    int head = 0;
    State current_state = q0;
    
    // Abrir archivo en modo escritura (borra contenido anterior)
    FILE *file = fopen("traza_tm.txt", "w");
    if (file == NULL) return 1;

    // Validación de argumentos
    if (argc < 2) {
        printf("Uso: ./tm_logic <cadena>\n");
        return 1;
    }
    
    strncpy(input, argv[1], 1000);
    input[1000] = '\0';

    // Inicializar cinta
    memset(tape, BLANK, MAX_LEN);
    strncpy(tape, input, strlen(input));
    // Importante: asegurar terminación limpia para la visualización
    tape[strlen(input)] = '\0'; 

    int steps = 0;
    // Bucle principal de la máquina
    while (current_state != q4 && current_state != REJECT && steps < 10000) {
        
        // Registrar estado actual antes de mover
        print_id(file, tape, head, current_state);
        
        char symbol = tape[head];
        if (symbol == '\0') symbol = BLANK; // Tratamiento de fin de cadena como Blanco
        
        // --- LOGICA DE TRANSICION (Igual a tu tabla) ---
        switch (current_state) {
            case q0:
                if (symbol == '0') { tape[head] = 'X'; current_state = q1; head++; }
                else if (symbol == 'Y') { tape[head] = 'Y'; current_state = q3; head++; }
                else current_state = REJECT;
                break;
            case q1:
                if (symbol == '0') { current_state = q1; head++; }
                else if (symbol == '1') { tape[head] = 'Y'; current_state = q2; head--; }
                else if (symbol == 'Y') { current_state = q1; head++; }
                else current_state = REJECT;
                break;
            case q2:
                if (symbol == '0') { current_state = q2; head--; }
                else if (symbol == 'X') { current_state = q0; head++; }
                else if (symbol == 'Y') { current_state = q2; head--; }
                else current_state = REJECT;
                break;
            case q3:
                if (symbol == 'Y') { current_state = q3; head++; }
                else if (symbol == BLANK) { current_state = q4; head++; } // Aceptación
                else current_state = REJECT;
                break;
            default:
                current_state = REJECT; break;
        }
        
        // Si la cabeza se mueve a una zona negativa (crash) o muy lejos, ajustamos o expandimos
        if (head < 0) { current_state = REJECT; }
        if (head >= strlen(tape)) { 
            // Expandir cinta visualmente si es necesario, añadiendo un B real
            tape[head] = BLANK; 
            tape[head+1] = '\0'; 
        }

        steps++;
    }

    // Registrar estado final
    print_id(file, tape, head, current_state);
    
    fclose(file);
    return 0;
}