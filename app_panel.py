import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Archivo de persistencia de datos
ARCHIVO_DATOS = "control_mensual.csv"

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        df = pd.read_csv(ARCHIVO_DATOS)
        # Aseguramos que la columna Fecha sea formato datetime para poder filtrarla
        df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
        return df
    else:
        return pd.DataFrame(columns=["Fecha", "Categoría", "Tipo", "Descripción", "Medio de Pago", "Monto"])

def guardar_datos(df):
    df.to_csv(ARCHIVO_DATOS, index=False)

st.set_page_config(page_title="Control Mensual", layout="wide")
st.title("Panel de Control de Ingresos y Gastos")

df = cargar_datos()

# --- BARRA LATERAL: INGRESO DE DATOS ---
st.sidebar.header("Registrar Movimiento")

# El calendario permite escoger cualquier fecha sin restricciones
fecha = st.sidebar.date_input("Fecha", datetime.today())
categoria = st.sidebar.selectbox("Categoría", ["Ingreso", "Gasto"])

if categoria == "Ingreso":
    opciones_tipo = ["Ordinario", "Extraordinario"]
else:
    opciones_tipo = ["Gasto Fijo", "Gasto Variable", "Pago de Deudas"]

tipo = st.sidebar.selectbox("Tipo", opciones_tipo)
descripcion = st.sidebar.text_input("Descripción")
medio_pago = st.sidebar.selectbox("Medio de Pago", ["Efectivo", "Cuentas", "Billetera Digital", "Tarjeta de Crédito"])

# Ingreso manual del monto exacto sin porcentajes
monto = st.sidebar.number_input("Monto", min_value=0.0, format="%.2f", step=10.0)

submit = st.sidebar.button("Guardar Registro", type="primary", use_container_width=True)

if submit:
    if monto > 0:
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
        st.rerun()
    else:
        st.sidebar.error("El monto debe ser mayor a 0.")

# --- DASHBOARD PRINCIPAL ---
st.subheader("Resumen General")

# Convertimos la columna Fecha a datetime temporalmente para extraer mes y año
df_temp = df.copy()
df_temp['Fecha_DT'] = pd.to_datetime(df_temp['Fecha'])

# Filtros para el panel
col_filtro1, col_filtro2 = st.columns(2)

# Lista de años disponibles en los datos
if not df_temp.empty:
    años_disponibles = sorted(df_temp['Fecha_DT'].dt.year.unique().tolist())
else:
    años_disponibles = [datetime.today().year]

año_seleccionado = col_filtro1.selectbox("Filtrar por Año", ["Todos"] + años_disponibles)

meses = ["Todos", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
mes_seleccionado = col_filtro2.selectbox("Filtrar por Mes", meses)

# Aplicar los filtros a los datos
df_filtrado = df_temp.copy()

if año_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Fecha_DT'].dt.year == año_seleccionado]

if mes_seleccionado != "Todos":
    mes_numero = meses.index(mes_seleccionado) # Índice 1 al 12
    df_filtrado = df_filtrado[df_filtrado['Fecha_DT'].dt.month == mes_numero]

# Eliminamos la columna temporal para no ensuciar la tabla
df_filtrado = df_filtrado.drop(columns=['Fecha_DT'])

# Calcular saldos con los datos filtrados
ingresos_totales = df_filtrado[df_filtrado['Categoría'] == 'Ingreso']['Monto'].sum()
gastos_totales = df_filtrado[df_filtrado['Categoría'] == 'Gasto']['Monto'].sum()
saldo = ingresos_totales - gastos_totales

col1, col2, col3 = st.columns(3)
col1.metric("Total Ingresos", f"${ingresos_totales:,.2f}")
col2.metric("Total Gastos", f"${gastos_totales:,.2f}")
col3.metric("Saldo Neto", f"${saldo:,.2f}")

st.markdown("---")

# --- HISTORIAL Y GESTIÓN DE REGISTROS ---
st.subheader("Historial de Movimientos")
st.info("💡 **Tip:** Marca la casilla 'Seleccionar' para borrar registros. Los datos mostrados corresponden a los filtros aplicados arriba.")

# Preparamos la tabla visual usando los datos FILTRADOS
df_visual = df_filtrado.copy()
df_visual.insert(0, "Seleccionar", False)

columnas_datos = df.columns.tolist()
df_editado = st.data_editor(
    df_visual,
    use_container_width=True,
    hide_index=True,
    disabled=columnas_datos
)

# Identificamos el índice original de las filas seleccionadas en la vista filtrada
filas_seleccionadas_vista = df_editado[df_editado["Seleccionar"]].index

if len(filas_seleccionadas_vista) > 0:
    if st.button("🗑️ Eliminar Registros Seleccionados", type="primary"):
        # Se elimina usando el índice real del DataFrame original
        df = df.drop(filas_seleccionadas_vista).reset_index(drop=True)
        guardar_datos(df)
        st.success("¡Registros eliminados!")
        st.rerun()
