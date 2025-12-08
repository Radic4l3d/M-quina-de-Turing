"""
Script de prueba para la Máquina de Turing
"""

from turing_machine import TuringMachine, validate_input


def test_turing_machine():
    """Prueba la máquina de Turing con varios casos de prueba"""
    
    # Casos de prueba: (cadena, debe_aceptar)
    test_cases = [
        ("01", True),           # n=1
        ("0011", True),         # n=2
        ("000111", True),       # n=3
        ("00001111", True),     # n=4
        ("0000011111", True),   # n=5
        ("0", False),           # Solo 0
        ("1", False),           # Solo 1
        ("001", False),         # Más 0s que 1s
        ("0111", False),        # Más 1s que 0s
        ("10", False),          # Orden incorrecto
        ("0101", False),        # Alternados
        ("00110011", False),    # Patrón incorrecto
    ]
    
    print("=" * 80)
    print("PRUEBAS DE LA MÁQUINA DE TURING")
    print("Lenguaje: {0^n1^n | n >= 1}")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for input_string, should_accept in test_cases:
        print(f"Probando: '{input_string}' - Esperado: {'ACEPTAR' if should_accept else 'RECHAZAR'}")
        
        # Crear y ejecutar la máquina
        tm = TuringMachine()
        tm.load_tape(input_string)
        result = tm.run()
        
        # Verificar resultado
        if result == should_accept:
            print(f"  ✓ CORRECTO - {tm.get_result()}")
            passed += 1
        else:
            print(f"  ✗ INCORRECTO - {tm.get_result()}")
            failed += 1
        
        # Guardar salida
        filename = f"test_output_{input_string[:20]}.txt"
        tm.save_to_file(filename, input_string)
        print(f"  Salida guardada en: {filename}")
        print()
    
    print("=" * 80)
    print(f"Resultados: {passed} correctos, {failed} incorrectos")
    print("=" * 80)
    
    return failed == 0


def test_animation():
    """Prueba la animación con una cadena corta"""
    print("\n" + "=" * 80)
    print("PRUEBA DE ANIMACIÓN")
    print("=" * 80)
    
    input_string = "0011"
    print(f"\nAnimando cadena: '{input_string}'")
    
    tm = TuringMachine()
    tm.load_tape(input_string)
    tm.run()
    
    print(f"\nResultado: {tm.get_result()}")
    tm.animate(delay=0.3)


def test_validation():
    """Prueba la validación de entrada"""
    print("\n" + "=" * 80)
    print("PRUEBAS DE VALIDACIÓN")
    print("=" * 80)
    print()
    
    test_cases = [
        ("", False, "cadena vacía"),
        ("01", True, "cadena válida"),
        ("abc", False, "caracteres inválidos"),
        ("01a1", False, "contiene 'a'"),
        ("0" * 1001, False, "excede 1000 caracteres"),
        ("0" * 1000, True, "exactamente 1000 caracteres"),
    ]
    
    for input_string, should_be_valid, description in test_cases:
        is_valid, error_msg = validate_input(input_string)
        
        if is_valid == should_be_valid:
            print(f"✓ {description}: {'válida' if is_valid else 'inválida'}")
        else:
            print(f"✗ {description}: resultado inesperado")
            if error_msg:
                print(f"  Error: {error_msg}")


if __name__ == "__main__":
    # Ejecutar pruebas
    test_validation()
    print()
    
    all_passed = test_turing_machine()
    
    test_animation()
    
    if all_passed:
        print("\n✓ Todas las pruebas pasaron correctamente")
    else:
        print("\n✗ Algunas pruebas fallaron")
