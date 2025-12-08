import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import subprocess
import os
import sys

# --- CONFIGURACIÓN ---
C_EXECUTABLE = "tm_logic.exe" if os.name == 'nt' else "./tm_logic"
TRACE_FILE = "traza_tm.txt"

def run_c_simulation(input_str):
    """Compila (opcional) y ejecuta el programa en C"""
    # Paso opcional: Compilación automática si no existe el ejecutable
    if not os.path.exists(C_EXECUTABLE) and not os.path.exists("tm_logic"):
        print("Compilando código C...")
        os.system("gcc tm_logic.c -o tm_logic")
    
    print(f"Lanzando motor C con entrada: {input_str}")
    result = subprocess.run([C_EXECUTABLE, input_str], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error ejecutando el programa C.")
        sys.exit(1)

def parse_trace():
    """Lee el archivo generado por C y devuelve una lista de pasos"""
    steps = []
    if not os.path.exists(TRACE_FILE):
        return []
    
    with open(TRACE_FILE, 'r') as f:
        for line in f:
            try:
                # El C imprime: estado|cabeza|cinta
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    st = int(parts[0])
                    hd = int(parts[1])
                    tp = parts[2]
                    steps.append((st, hd, tp))
            except:
                pass
    return steps

# --- CONFIGURACIÓN DEL GRÁFICO (DIAGRAMA DE ESTADOS) ---
G = nx.DiGraph()
# Definimos los nodos y posiciones fijas para que se vea bonito
pos = {
    0: (0, 1),   # q0
    1: (1, 1),   # q1
    2: (1, 0),   # q2
    3: (0, 0),   # q3
    4: (-1, 0),  # q4 (Final)
    5: (0, -1)   # Reject (invisible o explícito)
}
states_map = {0: 'q0', 1: 'q1', 2: 'q2', 3: 'q3', 4: 'q4', 5: 'REJ'}
edge_labels = {
    (0, 1): '0/X, R', (0, 3): 'Y/Y, R',
    (1, 1): '0/0, R\nY/Y, R', (1, 2): '1/Y, L',
    (2, 2): '0/0, L\nY/Y, L', (2, 0): 'X/X, R',
    (3, 3): 'Y/Y, R', (3, 4): 'B/B, R'
}

for s in states_map.keys():
    G.add_node(s)
G.add_edges_from(edge_labels.keys())

# --- LÓGICA DE ANIMACIÓN ---
def animate_turing(user_input):
    # 1. Ejecutar Lógica C
    run_c_simulation(user_input)
    
    # 2. Leer Traza
    history = parse_trace()
    if not history:
        print("No se generó traza. Verifica el programa C.")
        return

    # 3. Preparar Figura
    fig, ax = plt.subplots(figsize=(10, 6))
    
    def update(frame_idx):
        ax.clear()
        
        # Datos del paso actual
        if frame_idx < len(history):
            state_idx, head_idx, tape_str = history[frame_idx]
        else:
            state_idx, head_idx, tape_str = history[-1]
            
        # -- DIBUJAR AUTÓMATA --
        # Colores: Gris normal, Rojo activo, Verde aceptación
        node_colors = []
        for node in G.nodes():
            if node == state_idx:
                node_colors.append('#ff5733' if node != 4 else '#33ff57') # Rojo activo, Verde final
            else:
                node_colors.append('#d3d3d3') # Gris inactivo

        # Dibujar nodos y aristas
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=800, edgecolors='black')
        nx.draw_networkx_labels(G, pos, ax=ax, labels=states_map)
        
        # Dibujar aristas curvas para que se vea mejor (connectionstyle)
        nx.draw_networkx_edges(G, pos, ax=ax, connectionstyle="arc3,rad=0.1", arrowstyle='-|>', arrowsize=20)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        # -- DIBUJAR CINTA (Como texto abajo) --
        # Formatear la cinta para resaltar la cabeza
        tape_display = ""
        pointer_display = ""
        
        # Ventana visual de la cinta (mostrar +/- 5 chars alrededor de la cabeza)
        start_view = max(0, head_idx - 6)
        end_view = min(len(tape_str), head_idx + 7)
        
        visible_tape = tape_str[start_view:end_view]
        
        # Construir visualización
        display_text = f"Paso: {frame_idx}\nEstado: {states_map.get(state_idx, 'UNK')}\n\n"
        
        # Cinta estilizada
        tape_chars = " | ".join(list(visible_tape))
        display_text += f"[ ... {tape_chars} ... ]\n"
        
        # Flecha indicadora
        # Calcular posición aproximada de la flecha es difícil en texto plano dentro de plot,
        # así que usaremos anotaciones relativas o simplemente marcaremos el símbolo.
        
        ax.set_title(f"Simulación MT: L = {{0^n 1^n}}\nEntrada: {user_input}", fontsize=14)
        
        # Texto de la cinta en la parte inferior del gráfico
        plt.text(0.5, -0.2, display_text, ha='center', va='center', transform=ax.transAxes, 
                 fontsize=12, fontfamily='monospace', bbox=dict(facecolor='white', alpha=0.8))

        # Texto del símbolo actual
        try:
            current_sym = tape_str[head_idx]
        except:
            current_sym = 'B'
        plt.text(0.5, -0.05, f"Leyendo: '{current_sym}'", ha='center', transform=ax.transAxes, color='blue', weight='bold')

        # Limitar ejes para que no se mueva el gráfico
        ax.set_xlim(-1.5, 2.5)
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')

    # Crear animación
    anim = FuncAnimation(fig, update, frames=len(history), interval=600, repeat=False)
    plt.show()

if __name__ == "__main__":
    print("--- Graficador de Máquina de Turing ---")
    user_in = input("Ingrese cadena (ej: 0011): ")
    animate_turing(user_in)