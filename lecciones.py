import tkinter as tk
import json
from estilos import COLOR_FONDO, COLOR_PRINCIPAL, COLOR_SECUNDARIO, COLOR_BOTON, COLOR_TEXTO
from estilos import FONT_TITULO, FONT_SUBTITULO, FONT_NORMAL, crear_boton

class LeccionesApp:
    def __init__(self, ventana, volver_callback):
        self.ventana = ventana
        self.volver_callback = volver_callback
        self.niveles = self.cargar_lecciones()
        self.mostrar_menu_lecciones()

    # Cargar lecciones desde JSON
    def cargar_lecciones(self):
        with open("data/lecciones.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["niveles"]

    # Limpiar ventana
    def limpiar_ventana(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    # MENÚ PRINCIPAL DE LECCIONES
    def mostrar_menu_lecciones(self):
        self.limpiar_ventana()
        tk.Label(
            self.ventana,
            text="🏆 Camino de Lecciones Financieras",
            font=FONT_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_PRINCIPAL
        ).pack(pady=20)

        for i, nivel in enumerate(self.niveles):
            texto = f"{i+1}. {nivel['nombre']} - {nivel['descripcion']}"
            crear_boton(
                self.ventana,
                texto,
                comando=lambda idx=i: self.mostrar_leccion(idx)
            ).pack(pady=5, fill="x", padx=60)

        crear_boton(
            self.ventana,
            "⬅ Volver al menú principal",
            comando=self.volver_callback,
            bg_color=COLOR_BOTON
        ).pack(pady=20)

    # LECCIÓN INDIVIDUAL
    def mostrar_leccion(self, idx):
        self.limpiar_ventana()
        nivel = self.niveles[idx]
        preguntas = nivel["preguntas"]
        total = len(preguntas)
        actual = {"i": 0, "score": 0}

        tk.Label(
            self.ventana,
            text=f"📘 {nivel['nombre']}",
            font=FONT_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_PRINCIPAL
        ).pack(pady=10)

        # Contenido educativo
        contenido_label = tk.Label(
            self.ventana,
            text=nivel.get("contenido", ""),
            font=FONT_NORMAL,
            wraplength=700,
            justify="left",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        contenido_label.pack(pady=20, padx=40)

        # Botón para iniciar quiz
        crear_boton(
            self.ventana,
            "▶ Comenzar lección",
            comando=lambda: self.comenzar_quiz(preguntas, total, actual)
        ).pack(pady=10, fill="x", padx=200)

        crear_boton(
            self.ventana,
            "⬅ Volver al menú principal",
            comando=self.volver_callback,
            bg_color=COLOR_BOTON
        ).pack(pady=20, fill="x", padx=200)

    # COMENZAR EL QUIZ
    def comenzar_quiz(self, preguntas, total, actual):
        self.limpiar_ventana()

        pregunta_label = tk.Label(
            self.ventana,
            text="",
            font=FONT_NORMAL,
            wraplength=700,
            justify="center",
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        pregunta_label.pack(pady=20)

        botones_frame = tk.Frame(self.ventana, bg=COLOR_FONDO)
        botones_frame.pack(pady=10)

        resultado_label = tk.Label(self.ventana, text="", font=FONT_NORMAL, bg=COLOR_FONDO)
        resultado_label.pack(pady=10)

        def mostrar_pregunta():
            for w in botones_frame.winfo_children():
                w.destroy()

            if actual["i"] >= total:
                self.mostrar_resultado(actual["score"], total)
                return

            p = preguntas[actual["i"]]
            pregunta_label.config(text=p["texto"])
            resultado_label.config(text="")

            for i, opcion in enumerate(p["opciones"]):
                crear_boton(
                    botones_frame,
                    opcion,
                    lambda i=i: responder(i)
                ).pack(pady=5, fill="x", padx=150)

        def responder(opcion_idx):
            p = preguntas[actual["i"]]
            if opcion_idx == p["respuesta"]:
                resultado_label.config(text="✅ Correcto", fg="green")
                actual["score"] += 1
            else:
                correcta = p['opciones'][p['respuesta']]
                resultado_label.config(
                    text=f"❌ Incorrecto. Respuesta correcta: {correcta}",
                    fg="red"
                )
            actual["i"] += 1
            self.ventana.after(1200, mostrar_pregunta)

        mostrar_pregunta()

    # RESULTADO FINAL
    def mostrar_resultado(self, aciertos, total):
        self.limpiar_ventana()

        tk.Label(
            self.ventana,
            text="🏁 Has completado la lección",
            font=FONT_TITULO,
            bg=COLOR_FONDO,
            fg=COLOR_PRINCIPAL
        ).pack(pady=20)

        tk.Label(
            self.ventana,
            text=f"Puntuación: {aciertos} de {total}",
            font=FONT_SUBTITULO,
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(pady=10)

        if aciertos == total:
            tk.Label(
                self.ventana,
                text="🏆 ¡Perfecto! Has ganado el trofeo de esta lección.",
                font=FONT_NORMAL,
                fg="green",
                bg=COLOR_FONDO
            ).pack(pady=10)
        else:
            tk.Label(
                self.ventana,
                text="💡 Sigue practicando para obtener el trofeo.",
                font=FONT_NORMAL,
                fg="orange",
                bg=COLOR_FONDO
            ).pack(pady=10)

        crear_boton(
            self.ventana,
            "⬅ Volver al menú principal",
            comando=self.volver_callback,
            bg_color=COLOR_BOTON
        ).pack(pady=20, fill="x", padx=200)
