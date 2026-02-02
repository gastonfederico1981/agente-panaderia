import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("🔍 Buscando modelos disponibles...")
try:
    # Listamos los modelos y vemos sus 'supported_actions'
    for m in client.models.list():
        if 'generateContent' in m.supported_actions:
            print(f"✅ Modelo encontrado: {m.name}")
except Exception as e:
    print(f"❌ Error al listar: {e}")