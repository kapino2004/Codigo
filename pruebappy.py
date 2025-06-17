import tkinter as tk
import random
from PIL import Image, ImageTk

# Funciones para mostrar/ocultar ventana principal
def ocultar_ventana_principal():
    root.withdraw()

def mostrar_ventana_principal():
    root.deiconify()

# =============== JUEGO 1: Piedra, Papel o Tijera ===============
def juego_ppt():
    ocultar_ventana_principal()
    ventana = tk.Toplevel()
    ventana.title("Piedra, Papel o Tijera")
    ventana.geometry("500x450")
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), mostrar_ventana_principal()))

    opciones = ['Piedra', 'Papel', 'Tijera']
    puntaje = {'Usuario': 0, 'PC': 0}

    imagenes = {
        'Piedra': ImageTk.PhotoImage(Image.open("piedra.png").resize((80, 80))),
        'Papel': ImageTk.PhotoImage(Image.open("papel.png").resize((80, 80))),
        'Tijera': ImageTk.PhotoImage(Image.open("tijera.png").resize((80, 80)))
    }

    def jugar(eleccion_usuario):
        eleccion_pc = random.choice(opciones)
        if eleccion_usuario == eleccion_pc:
            resultado = "Empate"
        elif (eleccion_usuario == 'Piedra' and eleccion_pc == 'Tijera') or \
             (eleccion_usuario == 'Papel' and eleccion_pc == 'Piedra') or \
             (eleccion_usuario == 'Tijera' and eleccion_pc == 'Papel'):
            resultado = "Ganaste"
            puntaje['Usuario'] += 1
        else:
            resultado = "Perdiste"
            puntaje['PC'] += 1

        img_usuario.config(image=imagenes[eleccion_usuario])
        img_pc.config(image=imagenes[eleccion_pc])
        img_usuario.image = imagenes[eleccion_usuario]
        img_pc.image = imagenes[eleccion_pc]

        etiqueta_resultado.config(
            text=f"{resultado}\nPuntaje: Tú {puntaje['Usuario']} - PC {puntaje['PC']}"
        )

    tk.Label(ventana, text="Elige tu opción:", font=("Arial", 16)).pack(pady=10)
    frame = tk.Frame(ventana)
    frame.pack()

    for opcion in opciones:
        tk.Button(frame, text=opcion, width=10, font=("Arial", 14),
                  command=lambda o=opcion: jugar(o)).pack(side=tk.LEFT, padx=10)

    # Imágenes
    frame_img = tk.Frame(ventana)
    frame_img.pack(pady=20)

    img_usuario = tk.Label(frame_img)
    img_usuario.pack(side=tk.LEFT, padx=30)

    img_pc = tk.Label(frame_img)
    img_pc.pack(side=tk.RIGHT, padx=30)

    etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 14), fg="blue")
    etiqueta_resultado.pack(pady=20)

# =============== JUEGO 2: Ahorcado ===============
def get_palabras():
    palabras = []
    with open("palabras_es.txt", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split()
            if len(partes) >= 1:
                palabra = partes[0].lower()
                if palabra.isalpha() and len(palabra) >= 5:
                    palabras.append(palabra)
    return palabras
        

def juego_ahorcado():
    ocultar_ventana_principal()
    ventana = tk.Toplevel()
    ventana.title("Ahorcado")
    ventana.geometry("500x450")
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), mostrar_ventana_principal()))

    palabras = get_palabras()
    palabra = random.choice(palabras)
    letras_adivinadas = []
    intentos = 6

    canvas = tk.Canvas(ventana, width=200, height=200, bg="white")
    canvas.pack(pady=10)

    def mostrar():
        return ' '.join([l if l in letras_adivinadas else '_' for l in palabra])

    def dibujar_monigote():
        partes = [
            lambda: canvas.create_oval(80, 20, 120, 60),
            lambda: canvas.create_line(100, 60, 100, 120),
            lambda: canvas.create_line(100, 80, 70, 100),
            lambda: canvas.create_line(100, 80, 130, 100),
            lambda: canvas.create_line(100, 120, 70, 150),
            lambda: canvas.create_line(100, 120, 130, 150),
        ]
        if intentos < 6:
            partes[5 - intentos]()

    def verificar(event=None):
        nonlocal intentos
        entrada_valor = entrada.get().lower().strip()
        entrada.delete(0, tk.END)

        if not entrada_valor.isalpha():
            mensaje.set("Ingresa solo letras.")
            return

        if len(entrada_valor) > 1:
            if entrada_valor == palabra:
                etiqueta_palabra.config(text=' '.join(palabra))
                mensaje.set("¡Ganaste! 🎉")
                entrada.config(state=tk.DISABLED)
                boton.config(state=tk.DISABLED)
            else:
                intentos -= 1
                mensaje.set(f"Palabra incorrecta. Intentos restantes: {intentos}")
                dibujar_monigote()
        else:
            letra = entrada_valor
            if letra in letras_adivinadas:
                mensaje.set("Ya intentaste esa letra.")
            elif letra in palabra:
                letras_adivinadas.append(letra)
                mensaje.set("¡Correcto!")
            else:
                letras_adivinadas.append(letra)
                intentos -= 1
                mensaje.set(f"Incorrecto. Intentos restantes: {intentos}")
                dibujar_monigote()

        etiqueta_palabra.config(text=mostrar())
        if '_' not in mostrar():
            mensaje.set("¡Ganaste! 🎉")
            entrada.config(state=tk.DISABLED)
            boton.config(state=tk.DISABLED)
        elif intentos == 0:
            mensaje.set(f"Perdiste. La palabra era: {palabra}")
            entrada.config(state=tk.DISABLED)
            boton.config(state=tk.DISABLED)

    etiqueta_palabra = tk.Label(ventana, text=mostrar(), font=("Courier", 24))
    etiqueta_palabra.pack(pady=10)

    entrada = tk.Entry(ventana, font=("Arial", 14), width=20)
    entrada.pack()
    entrada.bind("<Return>", verificar)

    boton = tk.Button(ventana, text="Verificar", command=verificar)
    boton.pack(pady=5)

    mensaje = tk.StringVar()
    tk.Label(ventana, textvariable=mensaje, font=("Arial", 12), fg="blue").pack(pady=10)


# =============== JUEGO 3: Snake ===============
def juego_snake():
    ocultar_ventana_principal()
    ventana = tk.Toplevel()
    ventana.title("Snake")
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana.destroy(), mostrar_ventana_principal()))

    TAM = 20
    ANCHO, ALTO = 400, 400

    class Snake:
        def _init_(self, ventana):
            self.canvas = tk.Canvas(ventana, width=ANCHO, height=ALTO, bg="black")
            self.canvas.pack()
            self.snake = [(100, 100), (80, 100), (60, 100)]
            self.direccion = 'Right'
            self.food = self.nueva_comida()
            self.puntos = 0
            ventana.bind("<KeyPress>", self.cambiar)
            self.mover()

        def nueva_comida(self):
            while True:
                x = random.randint(0, (ANCHO - TAM) // TAM) * TAM
                y = random.randint(0, (ALTO - TAM) // TAM) * TAM
                if (x, y) not in self.snake:
                    return (x, y)

        def cambiar(self, e):
            d = e.keysym
            op = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
            if d in op and self.direccion != op[d]:
                self.direccion = d

        def mover(self):
            x, y = self.snake[0]
            if self.direccion == 'Up': y -= TAM
            elif self.direccion == 'Down': y += TAM
            elif self.direccion == 'Left': x -= TAM
            elif self.direccion == 'Right': x += TAM
            nueva = (x, y)

            if nueva in self.snake or x < 0 or y < 0 or x >= ANCHO or y >= ALTO:
                self.canvas.create_text(200, 200, text=f"Fin del juego\nPuntos: {self.puntos}", fill="red", font=("Arial", 18))
                return

            self.snake.insert(0, nueva)
            if nueva == self.food:
                self.puntos += 1
                self.food = self.nueva_comida()
            else:
                self.snake.pop()

            self.dibujar()
            self.canvas.after(150, self.mover)

        def dibujar(self):
            self.canvas.delete(tk.ALL)
            for x, y in self.snake:
                self.canvas.create_rectangle(x, y, x+TAM, y+TAM, fill="green")
            fx, fy = self.food
            self.canvas.create_oval(fx, fy, fx+TAM, fy+TAM, fill="red")

    Snake(ventana)

# =============== JUEGO 4: Pong ===============
def juego_pong():
    ocultar_ventana_principal()
    v = tk.Toplevel()
    v.title("Pong")
    v.protocol("WM_DELETE_WINDOW", lambda: (v.destroy(), mostrar_ventana_principal()))

    ANCHO, ALTO, TAM = 600, 400, 80

    class Pong:
        def __init__(self, v):
            self.canvas = tk.Canvas(v, width=ANCHO, height=ALTO, bg="black")
            self.canvas.pack()
            self.pj = self.canvas.create_rectangle(20, 150, 30, 150 + TAM, fill="white")
            self.cpu = self.canvas.create_rectangle(ANCHO - 30, 150, ANCHO - 20, 150 + TAM, fill="white")
            self.bola = self.canvas.create_oval(290, 190, 310, 210, fill="red")
            self.dx, self.dy = 5, random.choice([-5, 5])
            self.canvas.bind_all("<Up>", self.arriba)
            self.canvas.bind_all("<Down>", self.abajo)
            self.p1, self.p2 = 0, 0
            self.texto = self.canvas.create_text(ANCHO // 2, 30, text="0 : 0", fill="white", font=("Arial", 24))
            self.actualizar()

        def mover_cpu(self):
            _, y1, _, y2 = self.canvas.coords(self.cpu)
            _, by1, _, by2 = self.canvas.coords(self.bola)
            mid_bola = (by1 + by2) / 2
            mid_cpu = (y1 + y2) / 2
            if mid_bola > mid_cpu and y2 < ALTO:
                self.canvas.move(self.cpu, 0, 5)
            elif mid_bola < mid_cpu and y1 > 0:
                self.canvas.move(self.cpu, 0, -5)

        def mover_bola(self):
            self.canvas.move(self.bola, self.dx, self.dy)
            bx1, by1, bx2, by2 = self.canvas.coords(self.bola)

            if by1 <= 0 or by2 >= ALTO:
                self.dy *= -1
            if self.choque(self.pj, self.bola) or self.choque(self.cpu, self.bola):
                self.dx *= -1
            if bx2 >= ANCHO:
                self.p1 += 1
                self.reiniciar()
            elif bx1 <= 0:
                self.p2 += 1
                self.reiniciar()

            if (self.p1 + self.p2) % 5 == 0 and (self.p1 + self.p2) != 0:
                self.dx += 1 if self.dx > 0 else -1

            self.canvas.itemconfig(self.texto, text=f"{self.p1} : {self.p2}")

        def choque(self, paleta, bola):
            px1, py1, px2, py2 = self.canvas.coords(paleta)
            bx1, by1, bx2, by2 = self.canvas.coords(bola)
            return px1 < bx2 and px2 > bx1 and py1 < by2 and py2 > by1

        def reiniciar(self):
            self.canvas.coords(self.bola, 290, 190, 310, 210)
            self.dx *= random.choice([-1, 1])
            self.dy = random.choice([-5, 5])

        def arriba(self, e):
            self.canvas.move(self.pj, 0, -20)

        def abajo(self, e):
            self.canvas.move(self.pj, 0, 20)

        def actualizar(self):
            self.mover_bola()
            self.mover_cpu()
            self.canvas.after(30, self.actualizar)

    Pong(v)

# =============== MENÚ PRINCIPAL ===============
root = tk.Tk()
root.title("Menú de Juegos")
root.geometry("400x500")

tk.Label(root, text="Selecciona un juego", font=("Arial", 18)).pack(pady=20)
tk.Button(root, text="Piedra, Papel o Tijera", width=30, height=2, command=juego_ppt).pack(pady=5)
tk.Button(root, text="Ahorcado", width=30, height=2, command=juego_ahorcado).pack(pady=5)
tk.Button(root, text="Snake", width=30, height=2, command=juego_snake).pack(pady=5)
tk.Button(root, text="Pong", width=30, height=2, command=juego_pong).pack(pady=5)

root.mainloop()