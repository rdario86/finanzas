import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Fondo de Reserva", page_icon="💰", layout="centered")

# Encabezado del reporte
st.title("Construcción de Fondo de Reserva")

# Barra lateral para parámetros en porcentajes
with st.sidebar:
    st.header("Parámetros")
    ingresos = st.number_input("Ingresos Mensuales ($)", min_value=0.0, value=4100.0, step=100.0)
    porc_gastos = st.number_input("% de Gastos Fijos", min_value=0.0, max_value=100.0, value=60.0, step=1.0) / 100.0
    porc_disponible = st.number_input("% Disponible para Ahorro", min_value=0.0, max_value=100.0, value=10.0, step=1.0) / 100.0
    meses_reserva = st.number_input("Meses de Reserva (Meta)", min_value=1, value=3, step=1)

# Cálculos dinámicos
gastos_fijos = ingresos * porc_gastos
ahorro_mensual = ingresos * porc_disponible
meta = gastos_fijos * meses_reserva
ingreso_req = gastos_fijos / porc_gastos if porc_gastos > 0 else 0

# Resumen de métricas
st.subheader("Resumen Financiero")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ingresos", f"${ingresos:,.2f}")
col2.metric("Gastos Fijos", f"${gastos_fijos:,.2f}")
col3.metric("Ahorro Mensual", f"${ahorro_mensual:,.2f}")
col4.metric("Meta Fondo", f"${meta:,.2f}")

# Explicación de la meta con los símbolos de dólar corregidos (\$)
st.write(f"Para lograr este nivel (manteniendo tus gastos fijos en **\${gastos_fijos:,.2f}**), tus ingresos deben ser de al menos **\${ingreso_req:,.2f}**.")
st.write(f"Tu meta total de fondo de reserva será de **\${meta:,.2f}**.")

st.subheader("Proyección a 12 Meses")

# Cálculos de proyección
total_12_meses = ahorro_mensual * 12
pct_meta = (total_12_meses / meta) if meta > 0 else 0
rep_meses = (total_12_meses / gastos_fijos) if gastos_fijos > 0 else 0

# Tabla de resultados principales
datos = {
    "Métrica": [
        "Ahorro Mensual", 
        "Total Proyectado (12 Meses)", 
        "% de la Meta Alcanzada", 
        "Meses de Gastos Cubiertos (REP)"
    ],
    "Valor": [
        f"${ahorro_mensual:,.2f}", 
        f"${total_12_meses:,.2f}", 
        f"{pct_meta:.1%}", 
        f"{rep_meses:.2f}"
    ]
}

df_resumen = pd.DataFrame(datos)
st.table(df_resumen)

# Tabla de proyección acumulada (en formato horizontal)
st.subheader("Evolución del Fondo de Reserva (Acumulado)")

meses_cols = [f"Mes {i}" for i in range(1, 13)]
acum_monto = [ahorro_mensual * i for i in range(1, 13)]

# Se crea el DataFrame pasando los montos como una fila y los meses como columnas
df_acumulado = pd.DataFrame([acum_monto], columns=meses_cols, index=["Ahorro Acumulado"])

# Se aplica el formato de moneda a todas las celdas
st.dataframe(
    df_acumulado.style.format("${:,.2f}"), 
    use_container_width=True
)
