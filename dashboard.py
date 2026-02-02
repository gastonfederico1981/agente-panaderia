import streamlit as st
import pandas as pd
import google.generativeai as genai
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# --- CONFIGURACIÓN ESTÉTICA ---

st.set_page_config(
    page_title="SmartInsight_Ia- Análisis Multirrubro", 
    page_icon="📊", 
    layout="wide"
)

st.title("📊 Panel de Inteligencia de Negocios")
st.markdown("### Análisis de tickets y optimización de ventas mediante IA")

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
        genai.configure(api_key=st.session_state.api_key_actual)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Eres el Auditor Senior de L Art du Data. Analiza esto: {state['data_summary']}"
        response = model.generate_content(prompt)
        return {"audit_report": response.text}
    except Exception as e:
        return {"audit_report": f"❌ Error de IA: {str(e)}"}

workflow = StateGraph(AgentState)
workflow.add_node("analizar", node_analista)
workflow.set_entry_point("analizar")
workflow.add_edge("analizar", END)
app_agente = workflow.compile(checkpointer=MemorySaver())

# --- BARRA LATERAL (MENÚ DE NAVEGACIÓN) ---
with st.sidebar:
    st.markdown("## 🛡️ Panel de Control")
    menu = st.radio("Módulos:", ["🏠 Inicio", "📊 Auditoría Activa", "💬 Consultoría AI"])
    st.divider()
    st.session_state.sucursal_seleccionada = st.selectbox("Sucursal:", SUCURSALES)
    st.session_state.api_key_actual = st.text_input("🔑 API Key", type="password")
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

    if archivos and st.session_state.api_key_actual:
        st.session_state.all_summary = ""
        for arc in archivos:
            df = pd.read_csv(arc, sep=None, engine='python', encoding='latin1')
            
            # Limpieza para archivos tipo Madero
            def limpiar(v):
                s = str(v).replace('$', '').replace('.', '').replace(',', '.').strip()
                try: return float(s)
                except: return 0.0

            cols_din = [c for c in df.columns if any(p in c.upper() for p in ['TOTAL', 'IMPORTE', 'NETO'])]
            for c in cols_din: df[c] = df[c].apply(limpiar)
            
            venta = df[cols_din].sum().max() if cols_din else 0.0
            st.session_state.all_summary += f"\nArchivo: {arc.name}\nVenta Total: ${venta:,.2f}\nDatos:\n{df.head(50).to_string()}"
            st.success(f"✅ {arc.name} procesado. Venta detectada: ${venta:,.2f}")

        if st.button("🚀 GENERAR REPORTE CON IA"):
            config = {"configurable": {"thread_id": "demo_1"}}
            res = app_agente.invoke({"data_summary": st.session_state.all_summary}, config)
            st.session_state.reporte_actual = res["audit_report"]

    if st.session_state.reporte_actual:
        st.markdown(st.session_state.reporte_actual)
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🗑️ Analizar Desperdicio"):
                st.warning("IA buscando patrones de mermas...")
        with c2:
            num = "5491112345678"
            link = f"https://wa.me/{num}?text=Auditoria%20Lista"
            st.markdown(f'<a href="{link}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">🟢 Enviar por WhatsApp</button></a>', unsafe_allow_html=True)

# --- MÓDULO 3: CONSULTORÍA AI ---
elif menu == "💬 Consultoría AI":
    st.header("🤖 Consultor Inteligente")
    st.caption("Haz preguntas específicas sobre los archivos cargados anteriormente.")
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if p := st.chat_input("¿Qué quieres saber sobre los datos?"):
        st.session_state.messages.append({"role": "user", "content": p})
        with st.chat_message("user"): st.markdown(p)
        
        with st.chat_message("assistant"):
            config = {"configurable": {"thread_id": "demo_1"}}
            ctx = f"DATOS: {st.session_state.all_summary}\nPREGUNTA: {p}"
            r = app_agente.invoke({"data_summary": ctx}, config)
            st.markdown(r["audit_report"])
            st.session_state.messages.append({"role": "assistant", "content": r["audit_report"]})