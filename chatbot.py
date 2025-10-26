import google.generativeai as genai
import os
from dotenv import load_dotenv

class ChatBot:
    def __init__(self, nombre="FinBot"):
        self.nombre = nombre

        # 🔹 Cargar variables del archivo .env
        load_dotenv("config/.env")
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("⚠️ No se encontró la API key. Agrega GEMINI_API_KEY en config/.env")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

        # 🔹 Cargar prompt inicial desde archivo
        prompt_path = os.path.join("config", "prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_inicial = f.read().strip()

        self.historial = [{"role": "user", "parts": [prompt_inicial]}]

    def responder(self, mensaje):
        try:
            self.historial.append({"role": "user", "parts": [mensaje]})
            response = self.model.generate_content(contents=self.historial)
            respuesta = response.text.strip()
            self.historial.append({"role": "model", "parts": [respuesta]})
            return respuesta
        except Exception as e:
            return f"No pude responder en este momento 🤖 ({e})"
