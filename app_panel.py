import streamlit as st
import pandas as pd
from datetime import datetime
import os
import io

# Archivo de persistencia de datos local
ARCHIVO_DATOS = "Control_Mensual.xlsx"

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        try:
            df = pd.read_excel(ARCHIVO_DATOS)
            df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
            return df
        except Exception as e:
            st.error(f"⚠️ Error al leer archivo local: {e}")
            return pd.DataFrame(columns=["Fecha", "Categoría", "Tipo", "Descripción", "Medio de Pago", "Monto"])
    else:
        return pd.DataFrame(columns=["Fecha", "Categoría", "Tipo", "Descripción", "Medio de Pago", "Monto"])

def guardar_datos(df):
    df.to_excel(ARCHIVO_DATOS, index=False, engine='openpyxl')

st.set_page_config(page_title="Control Mensual", layout="wide")
st.title("📊 Panel de Control de Ingresos y Gastos")

# --- BARRA LATERAL: IMPORTACIÓN Y RESPALDO ---
st.sidebar.header("Gestión de Base de Datos")

archivo_subido = st.sidebar.file_uploader("📂 Importar archivo anterior (.xlsx)", type=["xlsx"])

if archivo_subido is not None:
    try:
        df_importado = pd.read_excel(archivo_subido)
        df_importado['Fecha'] = pd.to_datetime(df_importado['Fecha']).dt.date
        guardar_datos(df_importado) 
        st.sidebar.success("¡Base de datos importada exitosamente!")
    except Exception as e:
        st.sidebar.error(f"Error al importar: {e}")

df = cargar_datos()

st.sidebar.markdown("---")

# --- BARRA LATERAL: INGRESO DE DATOS ---
st.sidebar.header("Registrar Movimiento")

fecha = st.sidebar.date_input("Fecha", datetime.today())
categoria = st.sidebar.selectbox("Categoría", ["Ingreso", "Gasto", "Reserva"])

# Se añadieron las opciones solicitadas para la categoría Reserva
if categoria == "Ingreso":
    opciones_tipo = ["Ordinario", "Extraordinario"]
elif categoria == "Gasto":
    opciones_tipo = ["Gasto Fijo", "Gasto Variable", "Pago de Deudas"]
else:
    opciones_tipo = ["Ahorro", "Fondo", "Inversión"]

tipo = st.sidebar.selectbox("Tipo", opciones_tipo)
descripcion = st.sidebar.text_input("Descripción")
medio_pago = st.sidebar.selectbox("Medio de Pago", ["Efectivo", "Cuentas", "Billetera Digital", "Tarjeta de Crédito"])
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
        st.success("¡Registro guardado en Excel exitosamente!")
        st.rerun()
    else:
        st.sidebar.error("El monto debe ser mayor a 0.")

# --- BOTÓN DE RESPALDO (Descarga) ---
st.sidebar.markdown("---")
st.sidebar.subheader("Exportar Datos")
st.sidebar.info("Recuerda descargar tu archivo antes de cerrar si estás en una nube pública.")

if os.path.exists(ARCHIVO_DATOS):
    with open(ARCHIVO_DATOS, "rb") as file:
        st.sidebar.download_button(
            label="📥 Descargar Excel Actualizado",
            data=file,
            file_name=f"Control_Mensual_{datetime.today().strftime('%d-%m-%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# --- DASHBOARD PRINCIPAL ---
st.subheader("Resumen General")

df_temp = df.copy()
if not df_temp.empty:
    df_temp['Fecha_DT'] = pd.to_datetime(df_temp['Fecha'])

# --- SECCIÓN DE FILTROS MÚLTIPLES ---
st.markdown("##### 🔍 Filtros de Búsqueda")
st.caption("Deja los campos en blanco para incluir todos los registros.")

col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)

if not df_temp.empty:
    años_disponibles = sorted(df_temp['Fecha_DT'].dt.year.unique().tolist())
    categorias_disp = sorted(df_temp['Categoría'].unique().tolist())
    medios_disp = sorted(df_temp['Medio de Pago'].unique().tolist())
else:
    años_disponibles, categorias_disp, medios_disp = [], [], []

meses_nombres = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

años_seleccionados = col_f1.multiselect("Año", años_disponibles)
meses_seleccionados = col_f2.multiselect("Mes", meses_nombres)
categorias_seleccionadas = col_f3.multiselect("Categoría", categorias_disp)

if categorias_seleccionadas:
    tipos_disp = sorted(df_temp[df_temp['Categoría'].isin(categorias_seleccionadas)]['Tipo'].unique().tolist())
    bloquear_tipo = False
    mensaje_tipo = ""
else:
    tipos_disp = []
    bloquear_tipo = True
    mensaje_tipo = "Selecciona una Categoría primero"

tipos_seleccionados = col_f4.multiselect("Tipo", tipos_disp, disabled=bloquear_tipo, help=mensaje_tipo)
medios_seleccionados = col_f5.multiselect("Medio de Pago", medios_disp)

# Aplicar los filtros condicionalmente
df_filtrado = df_temp.copy()

if not df_filtrado.empty:
    if años_seleccionados:
        df_filtrado = df_filtrado[df_filtrado['Fecha_DT'].dt.year.isin(años_seleccionados)]

    if meses_seleccionados:
        meses_numeros = [meses_nombres.index(m) + 1 for m in meses_seleccionados]
        df_filtrado = df_filtrado[df_filtrado['Fecha_DT'].dt.month.isin(meses_numeros)]
        
    if categorias_seleccionadas:
        df_filtrado = df_filtrado[df_filtrado['Categoría'].isin(categorias_seleccionadas)]
        
    if tipos_seleccionados:
        df_filtrado = df_filtrado[df_filtrado['Tipo'].isin(tipos_seleccionados)]
        
    if medios_seleccionados:
        df_filtrado = df_filtrado[df_filtrado['Medio de Pago'].isin(medios_seleccionados)]
    
    df_filtrado = df_filtrado.drop(columns=['Fecha_DT'])

# Cálculos de métricas con los datos filtrados
ingresos_totales = df_filtrado[df_filtrado['Categoría'] == 'Ingreso']['Monto'].sum() if not df_filtrado.empty else 0
gastos_totales = df_filtrado[df_filtrado['Categoría'] == 'Gasto']['Monto'].sum() if not df_filtrado.empty else 0
reservas_totales = df_filtrado[df_filtrado['Categoría'] == 'Reserva']['Monto'].sum() if not df_filtrado.empty else 0
saldo = ingresos_totales - gastos_totales

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Ingresos", f"${ingresos_totales:,.2f}")
col2.metric("Total Gastos", f"${gastos_totales:,.2f}")
col3.metric("Saldo Neto", f"${saldo:,.2f}")
col4.metric("Total Reservado", f"${reservas_totales:,.2f}")

st.markdown("---")

# --- HISTORIAL Y GESTIÓN DE REGISTROS ---
st.subheader("Historial de Movimientos")

if df.empty:
    st.info("La base de datos está vacía. Registra tu primer movimiento o importa un archivo Excel.")
else:
    df_visual = df_filtrado.copy()
    df_visual.insert(0, "Seleccionar", False)
    columnas_datos = df.columns.tolist()

    df_editado = st.data_editor(
        df_visual,
        use_container_width=True,
        hide_index=True,
        disabled=columnas_datos,
        column_config={
            "Monto": st.column_config.NumberColumn(
                "Monto",
                format="$ %.2f",
            )
        }
    )

    filas_seleccionadas_vista = df_editado[df_editado["Seleccionar"]].index

    if len(filas_seleccionadas_vista) > 0:
        if st.button("🗑️ Eliminar Registros Seleccionados", type="primary"):
            df = df.drop(filas_seleccionadas_vista).reset_index(drop=True)
            guardar_datos(df)
            st.success("¡Registros eliminados del archivo Excel!")
            st.rerun()
