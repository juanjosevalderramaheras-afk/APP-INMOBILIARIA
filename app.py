import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# CONFIGURACION DE LA PANTALLA MOVIL
st.set_page_config(
    page_title="Inmo-Agente CRM",
    page_icon="🏢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS para entorno móvil
st.markdown("""
<style>
.main { 
    background-color: #f8f9fa; 
}
.stButton>button { 
    width: 100%; 
    border-radius: 10px; 
}
.lead-card {
    padding: 15px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    margin-bottom: 15px;
    border-left: 5px solid #007bff;
}
.lead-card-qualified { 
    padding: 15px;
    background-color: white;
    border-radius: 12px;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    margin-bottom: 15px;
    border-left: 5px solid #25D366; 
}
</style>
""", unsafe_allow_html=True)

# CONFIGURACIÓN DE GOOGLE SHEETS
SPREADSHEET_ID = "1XtOM1L3J8An1Dx4RDaD2pQ-Kzch4zwW5S7kHjCLWahI"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_data(ttl=10)
def cargar_datos_desde_sheets():
    try:
       credenciales=Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
       cliente_gspread = gspread.authorize(credenciales)         
       cliente_gspread.open_by_key(SPREADShojaHEET_ID).sheet1   
       datos = hoja.get_all_records() 
       return pd.DataFrame(datos) 
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame()

# INTERFAZ DE LA APLICACIÓN
st.title("🏢 InmoExclusiva")
st.subheader("Panel de Leads IA")

df = cargar_datos_desde_sheets()

if df.empty:
    st.info("Esperando a que entren los primeros mensajes de clientes... La base de datos se está actualizando.")
else:
    # Mostrar los leads de forma limpia si la base de datos ya está conectada
    for index, row in df.iterrows():
        nombre = row.get("Nombre", "Cliente Anónimo")
        telefono = row.get("Teléfono", "Sin Teléfono")
        mensaje = row.get("Mensaje", "Sin Mensaje")
        estado = row.get("Estado", "Nuevo")
        
        clase_card = "lead-card-qualified" if estado == "Calificado" else "lead-card"
        
        st.markdown(f"""
        <div class="{clase_card}">
            <h4 style='margin:0; color:#333;'>👤 {nombre}</h4>
            <p style='margin:5px 0; color:#555;'><b>📞 Teléfono:</b> {telefono}</p>
            <p style='margin:5px 0; color:#555;'><b>💬 Mensaje:</b> {mensaje}</p>
            <p style='margin:5px 0; color:#666;'><b>📌 Estado:</b> {estado}</p>
        </div>
        """, unsafe_allow_html=True)
