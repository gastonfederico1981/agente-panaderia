import streamlit as st
from google import genai
from twilio.rest import Client

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard Ventas", page_icon="📊")
st.title("🚀 Panel de Control: Reportes IA")

# 2. Cargar las llaves desde los Secrets de Streamlit
# Asegurate que en el panel de Streamlit los nombres sean EXACTAMENTE estos
GEMINI_KEY = st.secrets["GEMINI_KEY"]
TWILIO_SID = st.secrets["TWILIO_SID"]
TWILIO_TOKEN = st.secrets["TWILIO_TOKEN"]
TWILIO_FROM = st.secrets["TWILIO_FROM"]
TWILIO_TO = st.secrets["TWILIO_TO"]

# Sidebar para cargar los datos
st.sidebar.header("Datos de Sucursales")
ticket_callao = st.sidebar.number_input("Ticket Callao ($)", value=4694)
ticket_petrona = st.sidebar.number_input("Ticket Petrona ($)", value=5723)

# 3. Configuración del Cliente Google (Usando la variable que cargamos arriba)
client_google = genai.Client(api_key=GEMINI_KEY)

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
            response = client_google.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            mensaje_ia = response.text
        
        st.success("✨ Mensaje de IA generado:")
        st.info(mensaje_ia)

        # B. Enviar por Twilio
        with st.spinner('📩 Enviando a WhatsApp...'):
            # Usamos las variables que definimos arriba con st.secrets
            client_twilio = Client(TWILIO_SID, TWILIO_TOKEN)
            
            message = client_twilio.messages.create(
                body=mensaje_ia,
                from_=TWILIO_FROM,
                to=TWILIO_TO
            )
            
        st.balloons()
        st.success(f"✅ ¡Enviado con éxito! (SID: {message.sid})")

    except Exception as e:
        st.error(f"❌ Ups, algo falló: {e}")