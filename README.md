# Máquina de Turing - Reconocedor del Lenguaje {0^n1^n | n >= 1}

## Descripción

Este programa implementa una Máquina de Turing que reconoce el lenguaje {0^n1^n | n >= 1}, basado en el ejercicio 8.2 del libro de John Hopcroft (segunda edición).

El lenguaje consiste en cadenas donde hay exactamente el mismo número de 0s seguidos de 1s, por ejemplo:
- **Aceptadas**: `01`, `0011`, `000111`, `00001111`, etc.
- **Rechazadas**: `0`, `1`, `001`, `0111`, `10`, `0101`, etc.

## Características

- ✅ Reconoce el lenguaje {0^n1^n | n >= 1}
- ✅ Acepta cadenas de hasta 1000 caracteres
- ✅ Genera archivos de salida con descripciones instantáneas de cada paso
- ✅ Animación visual para cadenas ≤ 10 caracteres
- ✅ Modo interactivo y modo de prueba automático

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
================================================================================
MÁQUINA DE TURING - Reconocedor del lenguaje {0^n1^n | n >= 1}
================================================================================

Cadena de entrada: 0011
Longitud: 4
Resultado: ACEPTADA
Total de pasos: 19

================================================================================
DESCRIPCIÓN INSTANTÁNEA DE CADA PASO
================================================================================

Paso 0:
  Descripción instantánea: Bq00011B
  Estado: q0
  Posición del cabezal: 1
  Símbolo leído: 0
  Cinta: B0011B

...
```

## Algoritmo de la Máquina de Turing

### Estados

- **q0**: Estado inicial - verifica que la cadena empiece con 0
- **q1**: Busca el primer 1 sin marcar
- **q2**: Regresa al inicio de la cinta
- **q3**: Busca el siguiente 0 sin marcar
- **q4**: Verificación final - comprueba que solo haya marcas
- **qa**: Estado de aceptación
- **qr**: Estado de rechazo

### Símbolos

- **0, 1**: Símbolos de entrada
- **X**: Marca un 0 procesado
- **Y**: Marca un 1 procesado
- **B**: Símbolo en blanco (blank)

### Funcionamiento

1. Marca el primer 0 con X
2. Busca y marca el primer 1 con Y
3. Regresa al inicio
4. Repite los pasos 1-3 hasta procesar todos los símbolos
5. Verifica que solo queden marcas X e Y (sin 0s o 1s sin marcar)
6. Acepta si la verificación es exitosa, rechaza en caso contrario

## Animación

Para cadenas de 10 caracteres o menos, el programa puede mostrar una animación visual paso a paso que incluye:

- Estado actual
- Descripción instantánea
- Visualización de la cinta con el cabezal marcado
- Pausa entre pasos para seguir la ejecución

Ejemplo de visualización:

```
--- Paso 2 ---
Estado: q1
Descripción instantánea: BX0q111B
Cinta:  B  X  0 [1] 1  B 
                  ^
                 (cabezal)
```

## Ejemplos de Uso

### Ejemplo 1: Cadena Válida

```bash
$ python3 turing_machine.py
Seleccione una opción (1 o 2): 1
Ingrese la cadena: 0011

Procesando cadena: '0011'
Resultado: ACEPTADA
Salida guardada en: output_0011.txt
```

### Ejemplo 2: Cadena Inválida

```bash
$ python3 turing_machine.py
Seleccione una opción (1 o 2): 1
Ingrese la cadena: 001

Procesando cadena: '001'
Resultado: RECHAZADA
Salida guardada en: output_001.txt
```

## Estructura del Proyecto

```
M-quina-de-Turing/
│
├── README.md                    # Este archivo
├── turing_machine.py            # Implementación principal
└── test_turing_machine.py       # Suite de pruebas
```

## Autor

Implementación basada en el ejercicio 8.2 del libro "Introduction to Automata Theory, Languages, and Computation" de John Hopcroft (segunda edición).

## Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.