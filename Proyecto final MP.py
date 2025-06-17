import tkinter as tk
from tkinter import messagebox
import random
import turtle
import threading

# ================== JUEGO 1: Piedra, Papel o Tijera ==================
def juego_ppt():
    ventana = tk.Toplevel()
    ventana.title("Piedra, Papel o Tijera")
    ventana.geometry("400x300")
    opciones = ['Piedra', 'Papel', 'Tijera']

    def jugar(eleccion_usuario):
        eleccion_pc = random.choice(opciones)
        if eleccion_usuario == eleccion_pc:
            resultado = "Empate"
        elif (eleccion_usuario == 'Piedra' and eleccion_pc == 'Tijera') or \
             (eleccion_usuario == 'Papel' and eleccion_pc == 'Piedra') or \
             (eleccion_usuario == 'Tijera' and eleccion_pc == 'Papel'):
            resultado = "Ganaste"
        else:
            resultado = "Perdiste"
        etiqueta_resultado.config(
            text=f"Tú: {eleccion_usuario} | PC: {eleccion_pc} → {resultado}"
        )

    tk.Label(ventana, text="Elige tu opción:", font=("Arial", 16)).pack(pady=10)
    frame = tk.Frame(ventana)
    frame.pack()
    for opcion in opciones:
        tk.Button(
            frame,
            text=opcion,
            width=10,
            font=("Arial", 14),
            command=lambda o=opcion: jugar(o)
        ).pack(side=tk.LEFT, padx=10)

    etiqueta_resultado = tk.Label(ventana, text="", font=("Arial", 14), fg="blue")
    etiqueta_resultado.pack(pady=30)

# ================== JUEGO 2: Ahorcado ==================
def juego_ahorcado():
    ventana = tk.Toplevel()
    ventana.title("Ahorcado")
    ventana.geometry("400x300")

    palabras = ['python', 'juego', 'programa', 'tkinter', 'ventana']
    palabra = random.choice(palabras)
    letras_adivinadas = []

    def actualizar_palabra():
        texto = ' '.join([letra if letra in letras_adivinadas else '_' for letra in palabra])
        etiqueta_palabra.config(text=texto)
        if '_' not in texto:
            messagebox.showinfo("Ganaste", "¡Adivinaste la palabra!")

    def intentar():
        letra = entrada.get().lower()
        if letra and letra not in letras_adivinadas:
            letras_adivinadas.append(letra)
            actualizar_palabra()
        entrada.delete(0, tk.END)

    etiqueta_instruccion = tk.Label(ventana, text="Adivina la palabra:", font=("Arial", 14))
    etiqueta_instruccion.pack(pady=10)
    etiqueta_palabra = tk.Label(ventana, font=("Arial", 18))
    etiqueta_palabra.pack(pady=10)
    actualizar_palabra()

    entrada = tk.Entry(ventana, font=("Arial", 14))
    entrada.pack(pady=5)
    tk.Button(ventana, text="Intentar", command=intentar).pack(pady=5)

# ================== JUEGO 3: Snake ==================
def juego_snake():
    def ejecutar_snake():
        wn = turtle.Screen()
        wn.title("Snake")
        wn.bgcolor("black")
        wn.setup(width=600, height=600)
        wn.tracer(0)

        cabeza = turtle.Turtle()
        cabeza.speed(0)
        cabeza.shape("square")
        cabeza.color("green")
        cabeza.penup()
        cabeza.goto(0, 0)
        cabeza.direction = "stop"

        def mover():
            if cabeza.direction == "up":
                y = cabeza.ycor()
                cabeza.sety(y + 20)
            if cabeza.direction == "down":
                y = cabeza.ycor()
                cabeza.sety(y - 20)
            if cabeza.direction == "left":
                x = cabeza.xcor()
                cabeza.setx(x - 20)
            if cabeza.direction == "right":
                x = cabeza.xcor()
                cabeza.setx(x + 20)

        def ir_arriba(): cabeza.direction = "up"
        def ir_abajo(): cabeza.direction = "down"
        def ir_izquierda(): cabeza.direction = "left"
        def ir_derecha(): cabeza.direction = "right"

        wn.listen()
        wn.onkeypress(ir_arriba, "w")
        wn.onkeypress(ir_abajo, "s")
        wn.onkeypress(ir_izquierda, "a")
        wn.onkeypress(ir_derecha, "d")

        while True:
            wn.update()
            mover()
            turtle.delay(100)

    threading.Thread(target=ejecutar_snake).start()

# ================== JUEGO 4: Pong ==================
def juego_pong():
    def ejecutar_pong():
        wn = turtle.Screen()
        wn.title("Pong")
        wn.bgcolor("black")
        wn.setup(width=800, height=600)

        raqueta_a = turtle.Turtle()
        raqueta_a.speed(0)
        raqueta_a.shape("square")
        raqueta_a.color("white")
        raqueta_a.shapesize(stretch_wid=6, stretch_len=1)
        raqueta_a.penup()
        raqueta_a.goto(-350, 0)

        raqueta_b = turtle.Turtle()
        raqueta_b.speed(0)
        raqueta_b.shape("square")
        raqueta_b.color("white")
        raqueta_b.shapesize(stretch_wid=6, stretch_len=1)
        raqueta_b.penup()
        raqueta_b.goto(350, 0)

        pelota = turtle.Turtle()
        pelota.speed(1)
        pelota.shape("circle")
        pelota.color("white")
        pelota.penup()
        pelota.goto(0, 0)
        pelota.dx = 2
        pelota.dy = -2

        def raqueta_a_arriba():
            y = raqueta_a.ycor()
            raqueta_a.sety(y + 20)

        def raqueta_a_abajo():
            y = raqueta_a.ycor()
            raqueta_a.sety(y - 20)

        def raqueta_b_arriba():
            y = raqueta_b.ycor()
            raqueta_b.sety(y + 20)

        def raqueta_b_abajo():
            y = raqueta_b.ycor()
            raqueta_b.sety(y - 20)

        wn.listen()
        wn.onkeypress(raqueta_a_arriba, "w")
        wn.onkeypress(raqueta_a_abajo, "s")
        wn.onkeypress(raqueta_b_arriba, "Up")
        wn.onkeypress(raqueta_b_abajo, "Down")

        while True:
            wn.update()
            pelota.setx(pelota.xcor() + pelota.dx)
            pelota.sety(pelota.ycor() + pelota.dy)

            if pelota.ycor() > 290:
                pelota.sety(290)
                pelota.dy *= -1
            if pelota.ycor() < -290:
                pelota.sety(-290)
                pelota.dy *= -1

            if pelota.xcor() > 390:
                pelota.goto(0, 0)
                pelota.dx *= -1
            if pelota.xcor() < -390:
                pelota.goto(0, 0)
                pelota.dx *= -1

            if (340 < pelota.xcor() < 350 and raqueta_b.ycor() - 50 < pelota.ycor() < raqueta_b.ycor() + 50):
                pelota.setx(340)
                pelota.dx *= -1

            if (-350 < pelota.xcor() < -340 and raqueta_a.ycor() - 50 < pelota.ycor() < raqueta_a.ycor() + 50):
                pelota.setx(-340)
                pelota.dx *= -1

    threading.Thread(target=ejecutar_pong).start()

# ================== MENÚ PRINCIPAL ==================
ventana_principal = tk.Tk()
ventana_principal.title("Mini Juegos - Marco Pino e Israel Farfán")
ventana_principal.geometry("400x400")

label_titulo = tk.Label(ventana_principal, text="Mini Juegos", font=("Arial", 20))
label_titulo.pack(pady=20)

btn_ppt = tk.Button(ventana_principal, text="Piedra, Papel o Tijera", command=juego_ppt, width=30)
btn_ppt.pack(pady=10)

btn_ahorcado = tk.Button(ventana_principal, text="Ahorcado", command=juego_ahorcado, width=30)
btn_ahorcado.pack(pady=10)

btn_snake = tk.Button(ventana_principal, text="Snake", command=juego_snake, width=30)
btn_snake.pack(pady=10)

btn_pong = tk.Button(ventana_principal, text="Pong", command=juego_pong, width=30)
btn_pong.pack(pady=10)

ventana_principal.mainloop()