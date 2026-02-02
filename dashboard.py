import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from typing import TypedDict  # <--- AGREGÁ ESTA LÍNEA
from dotenv import load_dotenv
from google.api_core import client_options

# Cargar variables de entorno (Localmente usa .env, en Render usa las de "Environment")
load_dotenv()
# Cambia esto al principio del dashboard.py
api_key = os.environ.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("Falta la GOOGLE_API_KEY. Por favor, configúrala en Render.")

# --- Tu lógica de la App de aquí en adelante ---
st.title("🚀 SmartInsight AI")
st.subheader("Análisis inteligente para tu negocio")

# --- INICIALIZACIÓN DE ESTADOS ---
if 'messages' not in st.session_state: st.session_state.messages = []
if 'reporte_actual' not in st.session_state: st.session_state.reporte_actual = ""
if 'all_summary' not in st.session_state: st.session_state.all_summary = ""

SUCURSALES = ["Sucursal Central", "Sucursal Mercado", "Sucursal San Telmo", "Sucursal Callao", "Sucursal Madero", "Sucursal Petrona", "Sucursal Malabia"]

# --- LÓGICA DE INTELIGENCIA ARTIFICIAL (Nodos) ---
class AgentState(TypedDict):
    data_summary: str
    audit_report: str

def node_analista(state: AgentState):
    try:
        llave = os.environ.get("GOOGLE_API_KEY")
        # Forzamos el endpoint estable v1
        options = client_options.ClientOptions(api_endpoint="generativelanguage.googleapis.com")
        genai.configure(api_key=llave, client_options=options)
        
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        
        prompt = f"Analiza estos datos de panadería: {state['data_summary']}"
        response = model.generate_content(prompt)
        
        return {"audit_report": response.text}
    except Exception as e:
        # Si falla, devolvemos el error pero permitimos que el flujo siga
        return {"audit_report": f"⚠️ Nota: La IA está en mantenimiento. Detalle: {str(e)}"}
# 1. Definimos la lógica que antes era un "nodo"
def ejecutar_agente(inputs):
    # Aquí llamas a tu función node_analista que ya tenías creada
    resultado = node_analista(inputs)
    return resultado

# 2. En lugar de app_agente = workflow.compile(), usamos una función simple
def app_agente_simple(input_text):
    # Simulamos el estado inicial que esperaba tu grafo
    estado_inicial = {"messages": [input_text]}
    return ejecutar_agente(estado_inicial)

# 3. Para la memoria (MemorySaver), usamos el st.session_state de Streamlit
if "historial" not in st.session_state:
    st.session_state.historial = []

# --- BARRA LATERAL (MENÚ DE NAVEGACIÓN) ---
with st.sidebar:
    st.markdown("## 🛡️ Panel de Control")
    menu = st.radio("Módulos:", ["🏠 Inicio", "📊 Auditoría Activa", "💬 Consultoría AI"])
    st.divider()
    st.session_state.sucursal_seleccionada = st.selectbox("Sucursal:", SUCURSALES)
    # ELIMINAMOS LA LÍNEA DE API_KEY_ACTUAL
    st.caption("L'Art du Data v2.0 - 2026")

# --- MÓDULO 1: INICIO ---
if menu == "🏠 Inicio":
    st.markdown('<p class="main-title">L\'Art du Data</p>', unsafe_allow_html=True)
    st.subheader(f"Bienvenido al sistema de control de la red de panaderías.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### ✅ ¿Qué auditamos hoy?
        * **Integridad de Ventas:** Cruzamos el reporte de Ayres con la realidad.
        * **Salud de Carga:** Detectamos empleados que no cargan precios o mermas.
        * **Fugas de Dinero:** Analizamos productos con venta cero.
        """)
    with col2:
        st.info(f"📍 **Sucursal en foco:** {st.session_state.sucursal_seleccionada}\n\nListo para procesar archivos de Enero 2026.")
    
    st.image("https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&q=80&w=1000", caption="Control de Calidad y Procesos")

# --- MÓDULO 2: AUDITORÍA ACTIVA ---
elif menu == "📊 Auditoría Activa":
    st.header("🔍 Análisis de Datos en Tiempo Real")
    archivos = st.file_uploader("Subir reportes CSV", type=["csv"], accept_multiple_files=True)

    if archivos:
        st.session_state.all_summary = ""
        for arc in archivos:
            # Detectar codificación y separador automáticamente
            df = pd.read_csv(arc, sep=None, engine='python', encoding='latin1')
            
            # Función de limpieza de moneda
            def limpiar(v):
                s = str(v).replace('$', '').replace('.', '').replace(',', '.').strip()
                try: return float(s)
                except: return 0.0

            # Identificar columnas de dinero
            cols_din = [c for c in df.columns if any(p in c.upper() for p in ['TOTAL', 'IMPORTE', 'NETO'])]
            for c in cols_din: 
                df[c] = df[c].apply(limpiar)
            
            venta = df[cols_din].sum().max() if cols_din else 0.0
            st.session_state.all_summary += f"\nArchivo: {arc.name}\nVenta Total: ${venta:,.2f}\nDatos:\n{df.head(10).to_string()}"
            st.success(f"✅ {arc.name} procesado. Venta: ${venta:,.2f}")

        # --- BOTÓN DE IA (Alineado correctamente) ---
        if st.button("🚀 GENERAR REPORTE CON IA"):
            with st.spinner("El Auditor IA está analizando los datos..."):
                # Llamada directa a la función sin LangGraph
                res = ejecutar_agente({"data_summary": st.session_state.all_summary})
                st.session_state.reporte_actual = res["audit_report"]

    if st.session_state.reporte_actual:
        st.markdown("### 📋 Reporte de Auditoría")
        st.markdown(st.session_state.reporte_actual)
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🗑️ Analizar Desperdicio"):
                st.warning("Buscando patrones de mermas...")
        with c2:
            num = "5491112345678" # Cambiá por tu número
            link = f"https://wa.me/{num}?text=Auditoria%20Lista"
            st.markdown(f'<a href="{link}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">🟢 Enviar por WhatsApp</button></a>', unsafe_allow_html=True)

# --- MÓDULO 3: CONSULTORÍA AI ---
elif menu == "💬 Consultoría AI":
    st.header("🤖 Consultor Inteligente")
    st.caption("Haz preguntas específicas sobre los archivos cargados anteriormente.")
    
    # Mostrar historial de chat
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): 
            st.markdown(m["content"])

    # Entrada del chat
    if p := st.chat_input("¿Qué quieres saber sobre los datos?"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): 
            st.markdown(p)
        
        with st.chat_message("assistant"):
            # Usamos el contexto de los datos cargados + la pregunta
            ctx = f"DATOS CARGADOS: {st.session_state.all_summary}\n\nPREGUNTA DEL USUARIO: {p}"
            
            # Llamamos a nuestra función liviana
            with st.spinner("Pensando..."):
                r = ejecutar_agente({"data_summary": ctx})
                respuesta_texto = r["audit_report"]
                
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})