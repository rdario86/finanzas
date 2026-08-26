import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Archivo de persistencia de datos
ARCHIVO_DATOS = "control_mensual.csv"

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        return pd.read_csv(ARCHIVO_DATOS)
    else:
        return pd.DataFrame(columns=["Fecha", "Categoría", "Tipo", "Descripción", "Medio de Pago", "Monto"])

def guardar_datos(df):
    df.to_csv(ARCHIVO_DATOS, index=False)

st.set_page_config(page_title="Control Mensual", layout="wide")
st.title("Panel de Control de Ingresos y Gastos")

df = cargar_datos()

# --- BARRA LATERAL: INGRESO DE DATOS ---
with st.sidebar.form("formulario_registro", clear_on_submit=True):
    st.header("Registrar Movimiento")
    fecha = st.date_input("Fecha", datetime.today())
    categoria = st.selectbox("Categoría", ["Ingreso", "Gasto"])
    tipo = st.selectbox("Tipo", ["Ordinario", "Extraordinario", "Gasto Fijo", "Gasto Variable", "Pago de Deudas"])
    descripcion = st.text_input("Descripción")
    
    medio_pago = st.selectbox("Medio de Pago", ["Efectivo", "Cuentas", "Billetera Digital", "Tarjeta de Crédito"])
    
    # Ingreso manual del monto exacto
    monto = st.number_input("Monto", min_value=0.0, format="%.2f", step=10.0)
    
    submit = st.form_submit_button("Guardar Registro")
    
    if submit:
        nuevo_registro = pd.DataFrame([{
            "Fecha": fecha.strftime("%Y-%m-%d"), 
            "Categoría": categoria, 
            "Tipo": tipo, 
            "Descripción": descripcion,
            "Medio de Pago": medio_pago,
            "Monto": monto
        }])
        df = pd.concat([df, nuevo_registro], ignore_index=True)
        guardar_datos(df)
        st.success("¡Registro guardado exitosamente!")
        st.rerun()

# --- DASHBOARD PRINCIPAL ---
st.subheader("Resumen General")

ingresos_totales = df[df['Categoría'] == 'Ingreso']['Monto'].sum()
gastos_totales = df[df['Categoría'] == 'Gasto']['Monto'].sum()
saldo = ingresos_totales - gastos_totales

col1, col2, col3 = st.columns(3)
col1.metric("Total Ingresos", f"${ingresos_totales:,.2f}")
col2.metric("Total Gastos", f"${gastos_totales:,.2f}")
col3.metric("Saldo Neto", f"${saldo:,.2f}")

st.markdown("---")

# --- HISTORIAL Y GESTIÓN DE REGISTROS (EDICIÓN INTERACTIVA) ---
st.subheader("Historial de Movimientos")
st.info("💡 **Tip:** Selecciona la casilla izquierda de una fila y presiona la papelera para eliminarla, o haz doble clic en cualquier celda para editar su contenido.")

# data_editor reemplaza a dataframe y permite la edición/eliminación nativa
df_editado = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic", # Esta propiedad habilita la selección y eliminación de filas
    hide_index=True
)

# Comparamos el DataFrame original con el editado. Si hay cambios, guardamos.
if not df.equals(df_editado):
    guardar_datos(df_editado)
    st.rerun() # Recarga para actualizar de inmediato los saldos en la parte superior
