import os
from dotenv import load_dotenv
from google import genai
from twilio.rest import Client

load_dotenv()

# Inicializamos el cliente (Asegurate que tu API KEY sea la de AI Studio)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def ejecutar():
    try:
        print("🤖 Consultando a Gemini 2.0 Flash...")
        
        # PROMPT SIMPLIFICADO
        txt_prompt = "Escribí un mensaje de WhatsApp para el equipo de Callao (Arg). Tienen un ticket bajo de $4,694 y tienen que llegar a $5,000 vendiendo combos. Sé motivador."

        # Llamada directa al modelo 2.0 (el más compatible con la nueva librería)
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=txt_prompt
        )
        
        mensaje_ia = response.text
        print(f"✨ IA generó: {mensaje_ia[:50]}...")

        # Envío por Twilio
        print("📩 Enviando a WhatsApp...")
        twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        
        message = twilio_client.messages.create(
            body=mensaje_ia,
            from_=os.getenv('NUMERO_TWILIO'),
            to=os.getenv('NUMERO_WHATSAPP_JEFE')
        )
        
        print(f"🚀 ¡ENVIADO! SID de Twilio: {message.sid}")

    except Exception as e:
        print(f"❌ Falló: {e}")

if __name__ == "__main__":
    ejecutar()