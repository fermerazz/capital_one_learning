import tkinter as tk
from lecciones import LeccionesApp
from chatbot import ChatBot
from desafio import DesafioApp
from estilos import COLOR_FONDO, COLOR_PRINCIPAL, COLOR_SECUNDARIO, COLOR_BOTON, COLOR_TEXTO
from estilos import FONT_TITULO, FONT_SUBTITULO, FONT_NORMAL, crear_boton

# MENÚ PRINCIPAL
def pantalla_inicio(ventana):
    ventana.title("Capital One Learning 💰")
    ventana.configure(bg=COLOR_FONDO)

    for widget in ventana.winfo_children():
        widget.destroy()

    tk.Label(
        ventana,
        text="Bienvenido a Capital One Learning 💰",
        font=FONT_TITULO,
        bg=COLOR_FONDO,
        fg=COLOR_PRINCIPAL
    ).pack(pady=60)

    # Botón Lecciones
    crear_boton(
        ventana,
        "📘 Lecciones",
        lambda: LeccionesApp(ventana, volver_callback=lambda: pantalla_inicio(ventana))
    ).pack(pady=15)

    # Botón Chat
    crear_boton(
        ventana,
        "💬 Chat con IA",
        lambda: mostrar_chat(ventana),
        bg_color=COLOR_BOTON
    ).pack(pady=15)

    # Botón Desafío vs IA
    crear_boton(
        ventana,
        "⚡ Desafío vs IA",
        lambda: DesafioApp(ventana, volver_callback=lambda: pantalla_inicio(ventana)),
        bg_color="#00cc66"  # verde acento
    ).pack(pady=15)

# CHAT
def mostrar_chat(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

    bot = ChatBot()

    tk.Label(
        ventana,
        text="💬 Chat con Capitan One",
        font=FONT_SUBTITULO,
        bg=COLOR_FONDO,
        fg=COLOR_PRINCIPAL
    ).pack(pady=10)

    chat_frame = tk.Frame(ventana, bg=COLOR_FONDO)
    chat_frame.pack(expand=True, fill="both", pady=10)

    chat_text = tk.Text(
        chat_frame,
        wrap="word",
        state="disabled",
        font=FONT_NORMAL,
        bg="white",
        fg=COLOR_TEXTO,
        bd=2,
        relief="groove",
        height=18
    )
    chat_text.pack(expand=True, fill="both", padx=20, pady=10)

    entrada = tk.Entry(ventana, font=FONT_NORMAL)
    entrada.pack(padx=40, pady=10, fill="x")

    def enviar_mensaje(event=None):
        mensaje = entrada.get().strip()
        if not mensaje:
            return
        chat_text.config(state="normal")
        chat_text.insert("end", f"Tú: {mensaje}\n")
        respuesta = bot.responder(mensaje)
        chat_text.insert("end", f"{bot.nombre}: {respuesta}\n\n")
        chat_text.config(state="disabled")
        chat_text.see("end")
        entrada.delete(0, "end")

    entrada.bind("<Return>", enviar_mensaje)
    crear_boton(ventana, "Enviar", enviar_mensaje, bg_color=COLOR_SECUNDARIO).pack(pady=5)
    crear_boton(ventana, "⬅ Volver", lambda: pantalla_inicio(ventana), bg_color=COLOR_BOTON).pack(pady=5)

# INICIO DE LA APP
def iniciar_app():
    ventana = tk.Tk()
    ventana.attributes("-fullscreen", True)
    pantalla_inicio(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    iniciar_app()
