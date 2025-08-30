# test_gemini.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"Chave: {GEMINI_API_KEY}")
print(f"Chave válida: {bool(GEMINI_API_KEY)}")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("Configuração do Gemini OK")
    
    # Tenta listar modelos disponíveis
    models = genai.list_models()
    print("Modelos disponíveis:")
    for model in models:
        print(f" - {model.name}")
        
except Exception as e:
    print(f"Erro na configuração: {e}")


