import tkinter as tk
import random
import json
from estilos import COLOR_FONDO, COLOR_PRINCIPAL, COLOR_SECUNDARIO, COLOR_BOTON, COLOR_TEXTO
from estilos import FONT_SUBTITULO, FONT_NORMAL, crear_boton

class DesafioApp:
    def __init__(self, ventana, volver_callback):
        self.ventana = ventana
        self.volver_callback = volver_callback
        self.niveles = self.cargar_preguntas()
        self.tiempo_por_pregunta = 10  # segundos
        self.timer_id = None
        self.mostrar_menu_desafio()

    def cargar_preguntas(self):
        with open("data/lecciones.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        preguntas = []
        for nivel in data["niveles"]:
            for p in nivel["preguntas"]:
                preguntas.append(p)
        random.shuffle(preguntas)
        return preguntas

    def limpiar_ventana(self):
        # Cancelar cualquier timer pendiente
        if self.timer_id:
            self.ventana.after_cancel(self.timer_id)
            self.timer_id = None
        for w in self.ventana.winfo_children():
            w.destroy()

    def mostrar_menu_desafio(self):
        self.limpiar_ventana()
        tk.Label(
            self.ventana,
            text="⚡ Desafío vs IA",
            font=FONT_SUBTITULO,
            bg=COLOR_FONDO,
            fg=COLOR_PRINCIPAL
        ).pack(pady=20)

        crear_boton(
            self.ventana,
            "▶ Comenzar Desafío",
            comando=self.comenzar_desafio
        ).pack(pady=10, fill="x", padx=200)

        crear_boton(
            self.ventana,
            "⬅ Volver al menú principal",
            comando=self.volver_callback,
            bg_color=COLOR_BOTON
        ).pack(pady=10, fill="x", padx=200)

    def comenzar_desafio(self):
        self.limpiar_ventana()
        self.score = 0
        self.i = 0
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        if self.i >= len(self.niveles):
            self.mostrar_resultado()
            return

        self.limpiar_ventana()
        p = self.niveles[self.i]

        tk.Label(
            self.ventana,
            text=p["texto"],
            font=FONT_NORMAL,
            wraplength=700,
            justify="center",
            bg=COLOR_FONDO,
            fg=COLOR_PRINCIPAL
        ).pack(pady=20)

        self.botones_frame = tk.Frame(self.ventana, bg=COLOR_FONDO)
        self.botones_frame.pack(pady=10)

        self.resultado_label = tk.Label(
        self.ventana,
        text="",
        font=FONT_NORMAL,
        bg=COLOR_FONDO,
        fg=COLOR_PRINCIPAL  # ← texto azul visible
    )
        self.resultado_label.pack(pady=10)


        for idx, opcion in enumerate(p["opciones"]):
            crear_boton(
                self.botones_frame,
                opcion,
                comando=lambda i=idx: self.responder(i)
            ).pack(pady=5, fill="x", padx=150)

        # Timer
        self.tiempo_restante = self.tiempo_por_pregunta
        self.timer_label = tk.Label(
        self.ventana,
        text=f"⏱ Tiempo: {self.tiempo_restante}s",
        font=FONT_NORMAL,
        bg=COLOR_FONDO,
        fg=COLOR_PRINCIPAL  # ← color visible en macOS
    )

        self.timer_label.pack(pady=5)
        self.actualizar_timer()

    def actualizar_timer(self):
        if self.tiempo_restante <= 0:
            if hasattr(self, 'resultado_label'):
                self.resultado_label.config(text="⏰ Tiempo agotado", fg="red")
            self.i += 1
            self.timer_id = self.ventana.after(1000, self.mostrar_pregunta)
        else:
            if hasattr(self, 'timer_label'):
                self.timer_label.config(text=f"Tiempo: {self.tiempo_restante}s")
            self.tiempo_restante -= 1
            self.timer_id = self.ventana.after(1000, self.actualizar_timer)

    def responder(self, opcion_idx):
        if not hasattr(self, 'resultado_label'):
            return
        p = self.niveles[self.i]
        if opcion_idx == p["respuesta"]:
            self.resultado_label.config(text="✅ Correcto", fg="green")
            self.score += 1
        else:
            correcta = p['opciones'][p['respuesta']]
            self.resultado_label.config(
                text=f"❌ Incorrecto. Respuesta correcta: {correcta}",
                fg="red"
            )
        self.i += 1
        self.timer_id = self.ventana.after(800, self.mostrar_pregunta)

    def mostrar_resultado(self):
        self.limpiar_ventana()
        tk.Label(
            self.ventana,
            text="🏁 Desafío completado",
            font=FONT_SUBTITULO,
            bg=COLOR_FONDO,
            fg=COLOR_PRINCIPAL
        ).pack(pady=20)

        tk.Label(
            self.ventana,
            text=f"Puntuación: {self.score} de {len(self.niveles)}",
            font=FONT_NORMAL,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(pady=10)

        crear_boton(
            self.ventana,
            "⬅ Volver al menú principal",
            comando=self.volver_callback,
            bg_color=COLOR_BOTON
        ).pack(pady=20, fill="x", padx=200)
