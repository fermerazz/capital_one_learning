
import tkinter as tk

# Colores
COLOR_FONDO = "#f5f8fa"
COLOR_PRINCIPAL = "#0047bb"
COLOR_SECUNDARIO = "#00a9e0"
COLOR_BOTON = "#ff6600"
COLOR_TEXTO = "#333333"

# Fuentes
FONT_TITULO = ("Arial", 22, "bold")
FONT_SUBTITULO = ("Arial", 16, "bold")
FONT_NORMAL = ("Arial", 12)

# Función para crear botones estilizados
def crear_boton(parent, text, comando, bg_color=COLOR_PRINCIPAL):
    label = tk.Label(
        parent,
        text=text,
        font=FONT_SUBTITULO,
        bg=bg_color,
        fg="white",
        padx=25,
        pady=12,
        relief="raised",
        bd=2,
        cursor="hand2"
    )
    label.bind("<Button-1>", lambda e: comando())
    label.bind("<Enter>", lambda e: label.config(bg=COLOR_SECUNDARIO))
    label.bind("<Leave>", lambda e: label.config(bg=bg_color))
    return label
