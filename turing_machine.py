"""
Máquina de Turing para reconocer el lenguaje {0^n1^n | n >= 1}
Basado en el ejercicio 8.2 del libro de John Hopcroft (segunda edición)
"""

import time
import sys
from typing import List, Tuple, Dict, Optional


class TuringMachine:
    """
    Implementación de una Máquina de Turing que reconoce el lenguaje {0^n1^n | n >= 1}
    
    Estados:
    - q0: Estado inicial
    - q1: Buscar el primer 0 sin marcar
    - q2: Buscar el primer 1 sin marcar después del 0
    - q3: Regresar al inicio
    - q4: Verificación final
    - qa: Estado de aceptación
    - qr: Estado de rechazo
    
    Símbolos:
    - 0, 1: Símbolos de entrada
    - X: Marca para 0 procesado
    - Y: Marca para 1 procesado
    - B: Símbolo en blanco (blank)
    """
    
    def __init__(self):
        self.tape = []
        self.head = 0
        self.state = 'q0'
        self.steps = []
        self.blank_symbol = 'B'
        self.accept_state = 'qa'
        self.reject_state = 'qr'
        
        # Definir la función de transición
        # Formato: (estado_actual, símbolo_leído) -> (nuevo_estado, símbolo_escribir, dirección)
        # Dirección: 'R' = derecha, 'L' = izquierda, 'S' = sin movimiento
        self.transitions = self._define_transitions()
    
    def _define_transitions(self) -> Dict[Tuple[str, str], Tuple[str, str, str]]:
        """
        Define las transiciones de la máquina de Turing para reconocer {0^n1^n | n >= 1}
        
        Algoritmo:
        1. Marcar el primer 0 con X y buscar el primer 1 sin marcar
        2. Marcar el primer 1 con Y
        3. Regresar al inicio
        4. Repetir hasta que todos los 0s y 1s estén marcados
        5. Verificar que solo haya marcas X e Y
        """
        return {
            # Estado q0: inicio, verificar que empiece con 0
            ('q0', '0'): ('q1', 'X', 'R'),
            ('q0', 'Y'): ('qr', 'Y', 'S'),  # Ya hay Y al inicio, rechazar
            ('q0', '1'): ('qr', '1', 'S'),  # Empieza con 1, rechazar
            ('q0', 'B'): ('qr', 'B', 'S'),  # Cadena vacía, rechazar
            ('q0', 'X'): ('q4', 'X', 'R'),  # Todos los 0s marcados, verificar
            
            # Estado q1: buscar el primer 1 sin marcar
            ('q1', '0'): ('q1', '0', 'R'),  # Saltar 0s sin marcar
            ('q1', 'Y'): ('q1', 'Y', 'R'),  # Saltar 1s marcados
            ('q1', '1'): ('q2', 'Y', 'L'),  # Encontró un 1, marcarlo y regresar
            ('q1', 'B'): ('qr', 'B', 'S'),  # No hay 1s suficientes, rechazar
            ('q1', 'X'): ('q1', 'X', 'R'),  # Saltar 0s marcados
            
            # Estado q2: regresar al inicio
            ('q2', '0'): ('q2', '0', 'L'),
            ('q2', '1'): ('q2', '1', 'L'),
            ('q2', 'X'): ('q2', 'X', 'L'),
            ('q2', 'Y'): ('q2', 'Y', 'L'),
            ('q2', 'B'): ('q3', 'B', 'R'),  # Llegó al inicio
            
            # Estado q3: buscar el siguiente 0 sin marcar
            ('q3', 'X'): ('q3', 'X', 'R'),  # Saltar 0s marcados
            ('q3', '0'): ('q1', 'X', 'R'),  # Encontró un 0, marcarlo y buscar 1
            ('q3', 'Y'): ('q4', 'Y', 'R'),  # No hay más 0s, verificar
            ('q3', 'B'): ('qr', 'B', 'S'),  # No debería llegar aquí
            
            # Estado q4: verificación final - solo debe haber Y's y blank
            ('q4', 'Y'): ('q4', 'Y', 'R'),  # Saltar 1s marcados
            ('q4', 'B'): ('qa', 'B', 'S'),  # Todo correcto, aceptar
            ('q4', '1'): ('qr', '1', 'S'),  # Hay 1s sin marcar, rechazar (más 1s que 0s)
            ('q4', '0'): ('qr', '0', 'S'),  # No debería haber 0s aquí
            ('q4', 'X'): ('qr', 'X', 'S'),  # No debería haber X aquí
        }
    
    def load_tape(self, input_string: str):
        """Carga la cadena de entrada en la cinta"""
        if len(input_string) > 1000:
            raise ValueError("La cadena excede el límite de 1000 caracteres")
        
        # La cinta tendrá un espacio en blanco al inicio y al final
        self.tape = [self.blank_symbol] + list(input_string) + [self.blank_symbol]
        self.head = 1  # Comenzar en el primer símbolo de la entrada
        self.state = 'q0'
        self.steps = []
        
        # Guardar la configuración inicial
        self._save_step()
    
    def _save_step(self):
        """Guarda la descripción instantánea del paso actual"""
        # Crear la descripción instantánea en formato: tape_izq + estado + tape_der
        left_tape = ''.join(self.tape[:self.head])
        right_tape = ''.join(self.tape[self.head:])
        
        instantaneous_description = f"{left_tape}{self.state}{right_tape}"
        
        step_info = {
            'step': len(self.steps),
            'state': self.state,
            'head': self.head,
            'tape': self.tape.copy(),
            'symbol': self.tape[self.head] if 0 <= self.head < len(self.tape) else self.blank_symbol,
            'description': instantaneous_description
        }
        self.steps.append(step_info)
    
    def step(self) -> bool:
        """
        Ejecuta un paso de la máquina de Turing
        Retorna True si la máquina continúa, False si llega a un estado final
        """
        if self.state in [self.accept_state, self.reject_state]:
            return False
        
        # Extender la cinta si es necesario
        if self.head < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append(self.blank_symbol)
        
        current_symbol = self.tape[self.head]
        
        # Buscar la transición
        if (self.state, current_symbol) not in self.transitions:
            # No hay transición definida, ir al estado de rechazo
            self.state = self.reject_state
            self._save_step()
            return False
        
        new_state, write_symbol, direction = self.transitions[(self.state, current_symbol)]
        
        # Aplicar la transición
        self.tape[self.head] = write_symbol
        self.state = new_state
        
        # Mover el cabezal
        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1
        # 'S' significa no moverse
        
        # Guardar el paso
        self._save_step()
        
        return self.state not in [self.accept_state, self.reject_state]
    
    def run(self, max_steps: int = 10000) -> bool:
        """
        Ejecuta la máquina de Turing hasta que se detenga o alcance el máximo de pasos
        Retorna True si acepta, False si rechaza
        """
        steps_count = 0
        while self.step() and steps_count < max_steps:
            steps_count += 1
        
        if steps_count >= max_steps:
            self.state = self.reject_state
            return False
        
        return self.state == self.accept_state
    
    def get_result(self) -> str:
        """Retorna el resultado de la computación"""
        if self.state == self.accept_state:
            return "ACEPTADA"
        elif self.state == self.reject_state:
            return "RECHAZADA"
        else:
            return "EN EJECUCIÓN"
    
    def save_to_file(self, filename: str, input_string: str):
        """Guarda la computación completa en un archivo de texto"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("MÁQUINA DE TURING - Reconocedor del lenguaje {0^n1^n | n >= 1}\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Cadena de entrada: {input_string}\n")
            f.write(f"Longitud: {len(input_string)}\n")
            f.write(f"Resultado: {self.get_result()}\n")
            f.write(f"Total de pasos: {len(self.steps) - 1}\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("DESCRIPCIÓN INSTANTÁNEA DE CADA PASO\n")
            f.write("=" * 80 + "\n\n")
            
            for step_info in self.steps:
                f.write(f"Paso {step_info['step']}:\n")
                f.write(f"  Descripción instantánea: {step_info['description']}\n")
                f.write(f"  Estado: {step_info['state']}\n")
                f.write(f"  Posición del cabezal: {step_info['head']}\n")
                f.write(f"  Símbolo leído: {step_info['symbol']}\n")
                f.write(f"  Cinta: {''.join(step_info['tape'])}\n")
                f.write("\n")
            
            f.write("=" * 80 + "\n")
            f.write(f"ESTADO FINAL: {self.get_result()}\n")
            f.write("=" * 80 + "\n")
    
    def animate(self, delay: float = 0.5):
        """
        Muestra una animación de la ejecución de la máquina de Turing
        Solo para cadenas <= 10 caracteres
        """
        print("\n" + "=" * 80)
        print("ANIMACIÓN DE LA MÁQUINA DE TURING")
        print("=" * 80 + "\n")
        
        for i, step_info in enumerate(self.steps):
            print(f"\n--- Paso {step_info['step']} ---")
            print(f"Estado: {step_info['state']}")
            print(f"Descripción instantánea: {step_info['description']}")
            
            # Visualizar la cinta con el cabezal
            tape_display = ""
            for j, symbol in enumerate(step_info['tape']):
                if j == step_info['head']:
                    tape_display += f"[{symbol}]"
                else:
                    tape_display += f" {symbol} "
            
            print(f"Cinta: {tape_display}")
            print(f"       {' ' * (step_info['head'] * 3)}  ^")
            print(f"       {' ' * (step_info['head'] * 3)} (cabezal)")
            
            if i < len(self.steps) - 1:
                time.sleep(delay)
        
        print("\n" + "=" * 80)
        print(f"RESULTADO: {self.get_result()}")
        print("=" * 80 + "\n")


def validate_input(input_string: str) -> Tuple[bool, str]:
    """
    Valida que la cadena de entrada solo contenga 0s y 1s
    Retorna (es_válida, mensaje_error)
    """
    if not input_string:
        return False, "La cadena no puede estar vacía"
    
    if len(input_string) > 1000:
        return False, "La cadena excede el límite de 1000 caracteres"
    
    for char in input_string:
        if char not in ['0', '1']:
            return False, f"La cadena contiene un carácter inválido: '{char}'"
    
    return True, ""


def main():
    """Función principal del programa"""
    print("=" * 80)
    print("MÁQUINA DE TURING")
    print("Reconocedor del lenguaje {0^n1^n | n >= 1}")
    print("=" * 80)
    print()
    
    # Opción para el usuario: ingresar cadena o usar ejemplos predeterminados
    print("Opciones:")
    print("1. Ingresar una cadena manualmente")
    print("2. Usar ejemplos predeterminados")
    
    choice = input("\nSeleccione una opción (1 o 2): ").strip()
    
    test_strings = []
    
    if choice == '1':
        input_string = input("\nIngrese la cadena (solo 0s y 1s, máximo 1000 caracteres): ").strip()
        is_valid, error_msg = validate_input(input_string)
        
        if not is_valid:
            print(f"\nError: {error_msg}")
            return
        
        test_strings = [input_string]
    
    else:
        # Ejemplos predeterminados
        test_strings = [
            "01",           # n=1, debe aceptar
            "0011",         # n=2, debe aceptar
            "000111",       # n=3, debe aceptar
            "00001111",     # n=4, debe aceptar
            "0000011111",   # n=5, debe aceptar
            "0",            # Solo 0, debe rechazar
            "1",            # Solo 1, debe rechazar
            "001",          # Más 0s que 1s, debe rechazar
            "0111",         # Más 1s que 0s, debe rechazar
            "10",           # Orden incorrecto, debe rechazar
        ]
        print("\nUsando ejemplos predeterminados...")
    
    # Procesar cada cadena
    for input_string in test_strings:
        print(f"\n{'=' * 80}")
        print(f"Procesando cadena: '{input_string}'")
        print(f"{'=' * 80}")
        
        # Crear la máquina de Turing
        tm = TuringMachine()
        tm.load_tape(input_string)
        
        # Ejecutar la máquina
        result = tm.run()
        
        # Guardar en archivo
        filename = f"output_{input_string[:20]}.txt"
        tm.save_to_file(filename, input_string)
        print(f"\nResultado: {tm.get_result()}")
        print(f"Salida guardada en: {filename}")
        
        # Animar si la cadena tiene <= 10 caracteres
        if len(input_string) <= 10:
            animate_choice = input("\n¿Desea ver la animación? (s/n): ").strip().lower()
            if animate_choice == 's':
                tm.animate(delay=0.8)
    
    print("\n" + "=" * 80)
    print("Proceso completado.")
    print("=" * 80)


if __name__ == "__main__":
    main()
