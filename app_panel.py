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
with st.sidebar.form("formulario_registro"):
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
            "Fecha": fecha, 
            "Categoría": categoria, 
            "Tipo": tipo, 
            "Descripción": descripcion,
            "Medio de Pago": medio_pago,
            "Monto": monto
        }])
        df = pd.concat([df, nuevo_registro], ignore_index=True)
        guardar_datos(df)
        st.success("¡Registro guardado exitosamente!")
        st.rerun() # Recarga la página para actualizar los saldos de inmediato

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

# --- HISTORIAL Y GESTIÓN DE REGISTROS ---
st.subheader("Historial de Movimientos")

# Agregamos una columna de ID visual para que sea fácil identificar qué borrar
df_visual = df.copy()
df_visual.insert(0, 'ID', df_visual.index)

# Mostramos la tabla
st.dataframe(df_visual, use_container_width=True, hide_index=True)

# Sección desplegable para eliminar
with st.expander("🗑️ Eliminar un registro"):
    if not df.empty:
        # Usamos number_input para escribir el ID a borrar
        id_borrar = st.number_input("Escribe el ID del registro que deseas eliminar:", min_value=0, max_value=len(df)-1, step=1)
        
        if st.button("Confirmar Eliminación", type="primary"):
            # Eliminamos la fila y reiniciamos los índices
            df = df.drop(id_borrar).reset_index(drop=True)
            guardar_datos(df)
            st.success(f"Registro {id_borrar} eliminado.")
            st.rerun() # Actualiza la app automáticamente
    else:
        st.info("No hay registros en la base de datos.")
