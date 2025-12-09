# Máquina de Turing - Reconocedor del Lenguaje {0^n1^n | n >= 1}

## Descripción

Este programa implementa una Máquina de Turing que reconoce el lenguaje {0^n1^n | n >= 1}, basado en el ejercicio 8.2 del libro de John Hopcroft (segunda edición).

El lenguaje consiste en cadenas donde hay exactamente el mismo número de 0s seguidos de 1s, por ejemplo:
- **Aceptadas**: `01`, `0011`, `000111`, `00001111`, etc.
- **Rechazadas**: `0`, `1`, `001`, `0111`, `10`, `0101`, etc.

## Características

- [x] Reconoce el lenguaje {0^n1^n | n >= 1}
- [x] Acepta cadenas de hasta 1000 caracteres
- [x] Genera archivos de salida con descripciones instantáneas de cada paso
- [x] Animación visual para cadenas ≤ 10 caracteres
- [x] Modo interactivo y modo de prueba automático

## Requisitos

- Python 3.6 o superior

## Uso

### Modo Interactivo

```bash
python3 turing_machine.py
```

El programa le presentará dos opciones:

1. **Ingresar una cadena manualmente**: Puede introducir cualquier cadena de 0s y 1s (máximo 1000 caracteres)
2. **Usar ejemplos predeterminados**: Ejecuta automáticamente un conjunto de casos de prueba

### Modo de Prueba

Para ejecutar todas las pruebas automáticamente:

```bash
python3 test_turing_machine.py
```

Este script ejecuta:
- Pruebas de validación de entrada
- 12 casos de prueba con verificación automática
- Una demostración de animación

## Formato de Salida

El programa genera archivos de texto con el formato `output_<cadena>.txt` que contienen:

1. **Información general**:
   - Cadena de entrada
   - Longitud de la cadena
   - Resultado (ACEPTADA/RECHAZADA)
   - Total de pasos

2. **Descripción instantánea de cada paso**:
   - Descripción instantánea (formato: cinta_izquierda + estado + cinta_derecha)
   - Estado actual
   - Posición del cabezal
   - Símbolo leído
   - Contenido completo de la cinta

3. **Estado final**

### Ejemplo de Salida

```
