"""
Script de demostración de la Máquina de Turing
Ejecuta ejemplos sin interacción del usuario
"""

from turing_machine import TuringMachine


def run_demo():
    """Ejecuta una demostración completa de la Máquina de Turing"""
    
    print("=" * 80)
    print("DEMOSTRACIÓN DE LA MÁQUINA DE TURING")
    print("Reconocedor del lenguaje {0^n1^n | n >= 1}")
    print("=" * 80)
    print()
    
    # Ejemplos de demostración
    examples = [
        ("01", "n=1, cadena válida mínima"),
        ("0011", "n=2, cadena válida"),
        ("000111", "n=3, cadena válida"),
        ("0", "Solo 0, inválida"),
        ("1", "Solo 1, inválida"),
        ("10", "Orden incorrecto, inválida"),
        ("001", "Más 0s que 1s, inválida"),
        ("0111", "Más 1s que 0s, inválida"),
    ]
    
    for input_string, description in examples:
        print(f"\n{'=' * 80}")
        print(f"Ejemplo: '{input_string}' - {description}")
        print(f"{'=' * 80}")
        
        # Crear y ejecutar la máquina
        tm = TuringMachine()
        tm.load_tape(input_string)
        result = tm.run()
        
        print(f"\nResultado: {tm.get_result()}")
        print(f"Pasos ejecutados: {len(tm.steps) - 1}")
        
        # Guardar a archivo
        filename = f"demo_output_{input_string}.txt"
        tm.save_to_file(filename, input_string)
        print(f"Detalles guardados en: {filename}")
        
        # Mostrar animación solo para cadenas cortas
        if len(input_string) <= 6:
            print("\n--- Animación ---")
            tm.animate(delay=0.2)
    
    print("\n" + "=" * 80)
    print("DEMOSTRACIÓN COMPLETADA")
    print("=" * 80)
    print("\nSe han generado archivos de salida con las descripciones instantáneas")
    print("de cada computación.")


if __name__ == "__main__":
    run_demo()
