import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from twilio.rest import Client

# 1. Cargar credenciales del archivo .env
load_dotenv()

# Configuración visual de la página
st.set_page_config(page_title="Dashboard Ventas", page_icon="📊")
st.title("🚀 Panel de Control: Reportes IA")

# Sidebar para cargar los datos
st.sidebar.header("Datos de Sucursales")
ticket_callao = st.sidebar.number_input("Ticket Callao ($)", value=4694)
ticket_petrona = st.sidebar.number_input("Ticket Petrona ($)", value=5723)

# 2. Configuración del Cliente Google (AFUERA del try/except)
client_google = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

if st.button("Generar Informe y Enviar"):
    try:
        # A. Preparar el pedido para la IA
        prompt = f"""
        Sucursal Callao: ${ticket_callao}. Sucursal Petrona: ${ticket_petrona}.
        Escribí un mensaje motivador de WhatsApp para el equipo de Callao.
        Instalos a vender combos para llegar a los $5,000. 
        Tono argentino, profesional pero cercano.
        """
        
        with st.spinner('🤖 Gemini está analizando los datos...'):
            # Usamos gemini-2.0-flash que es el más estable hoy
            response = client_google.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            mensaje_ia = response.text
        
        st.success("✨ Mensaje de IA generado:")
        st.info(mensaje_ia)

        # B. Enviar por Twilio
        with st.spinner('📩 Enviando a WhatsApp...'):
            # Asegurate que tus credenciales en el .env estén perfectas
            client_twilio = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
            
            message = client_twilio.messages.create(
                body=mensaje_ia,
                from_=os.getenv('NUMERO_TWILIO'),
                to=os.getenv('NUMERO_WHATSAPP_JEFE')
            )
            
        st.balloons()
        st.success(f"✅ ¡Enviado con éxito! (SID: {message.sid})")

    except Exception as e:
        # Aquí es donde va el 'except' que te pedía el error
        st.error(f"❌ Ups, algo falló: {e}")