import time
import os
import sys

# Configuración
DELAY = 0.5  # Segundos entre pasos

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_tape(tape, head, state):
    """Renderiza la cinta y la posición de la cabeza"""
    clear_screen()
    print("=== SIMULACIÓN MÁQUINA DE TURING ===")
    print(f"Estado Actual: {state}")
    
    # Visualización de la cinta
    tape_display = ""
    pointer = ""
    
    for i, char in enumerate(tape):
        tape_display += f"[{char}]"
        if i == head:
            pointer += " ^ "
        else:
            pointer += "   "
            
    print(tape_display)
    print(pointer)
    print("====================================")

def run_turing_machine(input_str):
    if len(input_str) > 10:
        print("Error: Para la animación, la cadena debe ser <= 10 caracteres.")
        return

    # Inicialización
    tape = list(input_str) + ['B'] * 5 # Padding de blancos
    head = 0
    state = 'q0'
    
    while state != 'q4' and state != 'REJECT':
        print_tape(tape, head, state)
        time.sleep(DELAY)
        
        # Leer símbolo actual
        # Si la cabeza sale del array visual, añadimos más blancos dinámicamente
        if head >= len(tape):
            tape.append('B')
        
        symbol = tape[head]
        
        # Lógica de Transiciones (Idéntica a la tabla)
        next_state = 'REJECT'
        write_symbol = symbol
        move = 0 # -1 L, 1 R
        
        if state == 'q0':
            if symbol == '0':
                next_state, write_symbol, move = 'q1', 'X', 1
            elif symbol == 'Y':
                next_state, write_symbol, move = 'q3', 'Y', 1
            # 1 o B rechazan
                
        elif state == 'q1':
            if symbol == '0':
                next_state, write_symbol, move = 'q1', '0', 1
            elif symbol == '1':
                next_state, write_symbol, move = 'q2', 'Y', -1
            elif symbol == 'Y':
                next_state, write_symbol, move = 'q1', 'Y', 1
                
        elif state == 'q2':
            if symbol == '0':
                next_state, write_symbol, move = 'q2', '0', -1
            elif symbol == 'X':
                next_state, write_symbol, move = 'q0', 'X', 1
            elif symbol == 'Y':
                next_state, write_symbol, move = 'q2', 'Y', -1
                
        elif state == 'q3':
            if symbol == 'Y':
                next_state, write_symbol, move = 'q3', 'Y', 1
            elif symbol == 'B':
                next_state, write_symbol, move = 'q4', 'B', 1 # ACEPTACION
        
        # Aplicar cambios
        if next_state != 'REJECT':
            state = next_state
            tape[head] = write_symbol
            head += move
        else:
            state = 'REJECT'

    # Estado Final
    print_tape(tape, head, state)
    if state == 'q4':
        print("\n>>> CADENA ACEPTADA <<<")
    else:
        print("\n>>> CADENA RECHAZADA <<<")

if __name__ == "__main__":
    try:
        user_input = input("Ingrese cadena para animar (ej: 0011): ")
        run_turing_machine(user_input)
    except KeyboardInterrupt:
        print("\nSimulación interrumpida.")