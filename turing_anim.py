import tkinter as tk
from tkinter import messagebox
import time

# LÓGICA DE LA MÁQUINA DE TURING
class TuringLogic:
    def __init__(self, tape_input):
        self.tape = list(tape_input)
        self.head = 0
        self.state = 'q0'
        self.history = []
        self.status = "RUNNING" # RUNNING, ACCEPTED, REJECTED
        
    def get_char(self, index):
        if 0 <= index < len(self.tape):
            return self.tape[index]
        return 'B'

    def step(self):
        if self.status != "RUNNING":
            return False

        char_read = self.get_char(self.head)
        
        # Lógica de Transición
        next_state = 'REJECT'
        write_char = char_read
        move = 0 # -1 L, 1 R
        
        if self.state == 'q0':
            if char_read == '0':   next_state, write_char, move = 'q1', 'X', 1
            elif char_read == 'Y': next_state, write_char, move = 'q3', 'Y', 1
            
        elif self.state == 'q1':
            if char_read == '0':   next_state, write_char, move = 'q1', '0', 1
            elif char_read == '1': next_state, write_char, move = 'q2', 'Y', -1
            elif char_read == 'Y': next_state, write_char, move = 'q1', 'Y', 1
            
        elif self.state == 'q2':
            if char_read == '0':   next_state, write_char, move = 'q2', '0', -1
            elif char_read == 'X': next_state, write_char, move = 'q0', 'X', 1
            elif char_read == 'Y': next_state, write_char, move = 'q2', 'Y', -1
            
        elif self.state == 'q3':
            if char_read == 'Y':   next_state, write_char, move = 'q3', 'Y', 1
            elif char_read == 'B': next_state, write_char, move = 'q4', 'B', 1
        
        # Guardar descripción
        move_str = "Der" if move == 1 else "Izq"
        step_desc = f"Estado {self.state}: Lee '{char_read}' → Escribe '{write_char}', Mueve {move_str} → Nuevo {next_state}"
        
        # Ejecutar cambios
        if next_state != 'REJECT':
            # Expansión de cinta si es necesario
            if self.head >= len(self.tape):
                self.tape.append('B')
            
            self.tape[self.head] = write_char
            self.state = next_state
            self.head += move
            
            # Verificar aceptación
            if self.state == 'q4':
                self.status = "ACCEPTED"
            
            return step_desc
        else:
            self.status = "REJECTED"
            return f"Cadena RECHAZADA en estado {self.state} leyendo '{char_read}'"

# INTERFAZ GRÁFICA
class TuringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Máquina de Turing")
        self.root.geometry("900x500")
        self.root.configure(bg="#f0f0f0")

        # Variables de control
        self.logic = None
        self.is_running = False
        self.speed_ms = 500
        
        # --- SECCIÓN SUPERIOR: ENTRADA ---
        frame_top = tk.Frame(root, bg="#f0f0f0", pady=10)
        frame_top.pack()
        
        tk.Label(frame_top, text="Cadena de entrada:", bg="#f0f0f0", font=("Arial", 12)).pack(side=tk.LEFT)
        self.entry_input = tk.Entry(frame_top, font=("Arial", 12), width=20)
        self.entry_input.insert(0, "000111") # Valor por defecto
        self.entry_input.pack(side=tk.LEFT, padx=10)
        
        btn_start = tk.Button(frame_top, text="Cargar y Animar", command=self.start_simulation, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        btn_start.pack(side=tk.LEFT)

        # --- SECCIÓN MEDIA: VISUALIZACIÓN CINTA ---
        self.canvas = tk.Canvas(root, width=800, height=200, bg="white", highlightthickness=2, highlightbackground="#333")
        self.canvas.pack(pady=20)
        
        # --- SECCIÓN INFERIOR: CONTROLES Y ESTADO ---
        frame_controls = tk.Frame(root, bg="#f0f0f0")
        frame_controls.pack()
        
        self.btn_pause = tk.Button(frame_controls, text="Pausar / Reanudar", command=self.toggle_pause, state=tk.DISABLED, width=20)
        self.btn_pause.pack(side=tk.LEFT, padx=10)
        
        tk.Label(frame_controls, text="Velocidad:", bg="#f0f0f0").pack(side=tk.LEFT)
        # slider de velocidad
        #self.scale_speed = tk.Scale(frame_controls, from_=100, to=1000, orient=tk.HORIZONTAL, label="ms", length=200)
        #self.scale_speed.set(500)
        #self.scale_speed.pack(side=tk.LEFT, padx=10)
        
        self.lbl_status = tk.Label(root, text="Estado: Esperando...", font=("Courier", 12, "bold"), bg="#f0f0f0", fg="#333")
        self.lbl_status.pack(pady=10)
        
        self.lbl_tape_idx = tk.Label(root, text="Posición Cabeza: 0", bg="#f0f0f0")
        self.lbl_tape_idx.pack()

    def start_simulation(self):
        input_str = self.entry_input.get()
        # Validación básica
        for c in input_str:
            if c not in ['0', '1']:
                messagebox.showerror("Error", "La cadena solo debe contener 0s y 1s")
                return
        
        self.logic = TuringLogic(input_str)
        self.is_running = True
        self.btn_pause.config(state=tk.NORMAL)
        self.draw_tape()
        self.run_step()

    def toggle_pause(self):
        self.is_running = not self.is_running

    def run_step(self):
        if not self.logic: return
        
        delay = 700
        #delay = self.scale_speed.get()
        # Leer velocidad del slider
        if self.is_running and self.logic.status == "RUNNING":
            desc = self.logic.step()
            self.lbl_status.config(text=desc, fg="blue")
            self.lbl_tape_idx.config(text=f"Posición Cabeza: {self.logic.head}")
            self.draw_tape()
            
            if self.logic.status == "ACCEPTED":
                self.lbl_status.config(text=">>> CADENA ACEPTADA (q4) <<<", fg="green")
                self.is_running = False
            elif self.logic.status == "REJECTED":
                self.lbl_status.config(text=">>> CADENA RECHAZADA <<<", fg="red")
                self.is_running = False

        # Siguiente frame
        if self.logic.status == "RUNNING":
            self.root.after(delay, self.run_step)

    def draw_tape(self):
        self.canvas.delete("all")
        
        # Configuración geométrica
        cw = 60 # Ancho celda
        ch = 60 # Alto celda
        center_x = 400 # Centro del canvas (800 / 2)
        y_pos = 70
        
        # Dibujar CINTA (Vista relativa a la cabeza)
        # 6 celdas a la izquierda y 6 a la derecha
        radius = 6
        head = self.logic.head
        
        for i in range(-radius, radius + 1):
            tape_idx = head + i
            char = self.logic.get_char(tape_idx)
            
            x1 = center_x + (i * cw) - (cw / 2)
            y1 = y_pos
            x2 = x1 + cw
            y2 = y1 + ch
            
            # Colores según el caracter
            color_bg = "#eee"
            if char == 'X': color_bg = "#fffeb3" # Amarillo claro
            if char == 'Y': color_bg = "#b3ffb3" # Verde claro
            if char == 'B': color_bg = "#ddd"    # Gris (vacío)
            
            # Dibujar celda
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color_bg, outline="black")
            self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=char, font=("Arial", 20, "bold"))
            
            # Dibujar índice pequeño abajo
            self.canvas.create_text((x1+x2)/2, y2 + 15, text=str(tape_idx), font=("Arial", 8), fill="#666")

        # Dibujar CABEZA LECTORA (Fija en el centro)
        head_x = center_x
        head_y = y_pos - 10
        self.canvas.create_polygon(
            head_x - 10, head_y - 15, # Esq Sup Izq
            head_x + 10, head_y - 15, # Esq Sup Der
            head_x, head_y,           # Punta Abajo
            fill="#ff5722", outline="black"
        )
        self.canvas.create_text(head_x, head_y - 25, text=self.logic.state, font=("Arial", 12, "bold"), fill="#ff5722")

        # Decoración de máquina
        self.canvas.create_line(0, y_pos-2, 800, y_pos-2, width=2, fill="#333") # Riel superior
        self.canvas.create_line(0, y_pos+ch+2, 800, y_pos+ch+2, width=2, fill="#333") # Riel inferior

if __name__ == "__main__":
    root = tk.Tk()
    app = TuringApp(root)
    root.mainloop()