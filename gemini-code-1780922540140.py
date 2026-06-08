import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# CONFIGURACIÓN DE LA PANTALLA MÓVIL
st.set_page_config(
    page_title="Inmo-Agente CRM",
    page_icon="🏢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para entorno móvil
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #25D366; color: white; }
    .lead-card { 
        background-color: white; 
        padding: 15px; 
        border-radius: 12px; 
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05); 
        margin-bottom: 15px;
        border-left: 5px solid #007bff;
    }
    .lead-card-qualified { border-left: 5px solid #25D366; }
    </style>
""", unsafe_allowed_html=True)

SPREADSHEET_ID = "1XtOMlL3J8AnlDx4RDaD2pQ-Kzch4zwW5S7kHjCLWahI"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

@st.cache_data(ttl=10)
def cargar_datos_desde_sheets():
    try:
        credenciales = Credentials.from_service_account_file("credenciales.json", scopes=SCOPES)
        cliente_gspread = gspread.authorize(credenciales)
        hoja = cliente_gspread.open_by_key(SPREADSHEET_ID).sheet1
        datos = hoja.get_all_records()
        return pd.DataFrame(datos)
    except Exception as e:
        st.error("Configurando la base de datos...")
        return pd.DataFrame()

st.title("🏢 InmoExclusiva")
st.subheader("Panel de Leads IA")

df = cargar_datos_desde_sheets()

if df.empty:
    st.info("Esperando a que entren los primeros mensajes de clientes... La base de datos se está vinculando.")
else:
    total_leads = len(df)
    cualificados = len(df[df['Cualificado'].str.contains('SÍ', na=False)])

    col1, col2 = st.columns(2)
    col1.metric("Leads Totales", f"👥 {total_leads}")
    col2.metric("Cualificados", f"✅ {cualificados}")

    st.write("---")
    st.write("### 📥 Clientes Recientes")

    df_invertido = df.iloc[::-1]

    for index, row in df_invertido.iterrows():
        es_cualificado = "SÍ" in str(row['Cualificado'])
        clase_card = "lead-card-qualified" if es_cualificado else "lead-card"
        
        st.markdown(f"""
            <div class="{clase_card}">
                <h4>💬 Cliente: "{row['Mensaje Cliente']}"</h4>
                <p><b>💰 Presupuesto:</b> {row['Presupuesto Detectado']}</p>
                <p><b>🏦 Financiación:</b> {row['Financiacion']}</p>
                <p><b>⏱️ Plazo:</b> {row['Plazo Compra (Meses)']}</p>
                <p><b>🧠 Análisis IA:</b> <i>{row['Analisis Interno']}</i></p>
                <p><b>📅 Fecha:</b> {row['Timestamp']}</p>
            </div>
        """, unsafe_allowed_html=True)
        
        if es_cualificado:
            st.success("🔥 ¡Este cliente está listo para comprar!")
            st.link_button("🟢 Contactar por WhatsApp", "https://wa.me/?text=Hola!%20Soy%20Alejandro%20de%20InmoExclusiva.")
        else:
            st.warning("⚠️ Cliente en seguimiento o no cualificado.")
        st.write("")