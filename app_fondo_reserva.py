import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Fondo de Reserva", layout="wide")

st.title("Construcción de Fondo de Reserva")

# Barra lateral para parámetros interactivos
with st.sidebar:
    st.header("Parámetros")
    ingresos = st.number_input("Ingresos Mensuales ($)", min_value=0.0, value=4100.0, step=100.0)
    porc_gastos = st.slider("% de Gastos Fijos", 0.0, 100.0, 60.0) / 100.0
    porc_disponible = st.slider("% Disponible para Ahorro", 0.0, 100.0, 10.0) / 100.0
    meses_reserva = st.number_input("Meses de Reserva (Meta)", min_value=1, value=3, step=1)
    porc_meta = st.slider("% de la Meta a Ahorrar (Opción B)", 0.0, 100.0, 5.0) / 100.0

# Cálculos principales basados en la lógica del archivo Excel
gastos_fijos = ingresos * porc_gastos
ahorro_monto = ingresos * porc_disponible
meta = gastos_fijos * meses_reserva
ahorro_porcentaje = meta * porc_meta

# Resumen de métricas
st.subheader("Resumen Financiero")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ingresos", f"${ingresos:,.2f}")
col2.metric("Gastos Fijos", f"${gastos_fijos:,.2f}")
col3.metric("Disponible Ahorro", f"${ahorro_monto:,.2f}")
col4.metric("Meta Fondo", f"${meta:,.2f}")

# Explicación de la meta con formato específico
st.info(f"Para lograr este nivel de reserva (manteniendo tus gastos fijos en **\${gastos_fijos:,.2f}** por {meses_reserva} meses), tu meta de fondo debe ser de al menos **\${meta:,.2f}**.")
st.subheader("Proyección a 12 Meses: Comparación de Estrategias")

# Estrategia 1: Asignación por Monto Fijo (Disponible)
total_monto = ahorro_monto * 12
pct_meta_monto = (total_monto / meta) if meta > 0 else 0
rep_monto = (total_monto / gastos_fijos) if gastos_fijos > 0 else 0

# Estrategia 2: Asignación por Porcentaje de la Meta
total_porcentaje = ahorro_porcentaje * 12
pct_meta_porcentaje = (total_porcentaje / meta) if meta > 0 else 0
rep_porcentaje = (total_porcentaje / gastos_fijos) if gastos_fijos > 0 else 0

# Tabla comparativa
datos = {
    "Estrategia": ["Por Monto (Disponible)", "Por Porcentaje (de la Meta)"],
    "Ahorro Mensual": [ahorro_monto, ahorro_porcentaje],
    "Total 12 Meses": [total_monto, total_porcentaje],
    "% de la Meta Alcanzada": [pct_meta_monto, pct_meta_porcentaje],
    "Meses de Gastos Cubiertos (REP)": [rep_monto, rep_porcentaje]
}

df_resumen = pd.DataFrame(datos)
st.dataframe(df_resumen.style.format({
    "Ahorro Mensual": "${:,.2f}",
    "Total 12 Meses": "${:,.2f}",
    "% de la Meta Alcanzada": "{:.1%}",
    "Meses de Gastos Cubiertos (REP)": "{:.2f}"
}), use_container_width=True)

# Gráfico de proyección acumulada
st.subheader("Evolución del Fondo de Reserva (Acumulado)")
meses_labels = [f"Mes {i}" for i in range(1, 13)]

acum_monto = [ahorro_monto * i for i in range(1, 13)]
acum_porcentaje = [ahorro_porcentaje * i for i in range(1, 13)]

df_grafico = pd.DataFrame({
    "Por Monto": acum_monto,
    "Por Porcentaje": acum_porcentaje
}, index=meses_labels)

st.line_chart(df_grafico)
