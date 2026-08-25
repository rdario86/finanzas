import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diagnóstico Financiero", page_icon="📊", layout="wide")

# Encabezado personalizado
st.title("Diagnóstico Financiero 📊")
st.markdown("#### Panel de Control - Rubén Núñez")
st.markdown("Ingresa tus salidas mensuales actuales para evaluar tu estructura financiera.")

# Nueva Leyenda del Diagnóstico (Regla combinada)
with st.expander("ℹ️ Nueva Regla: ¿Cómo se evalúa el estatus financiero?"):
    st.markdown("""
    El estado de tus finanzas se determina evaluando el peso de tus **Gastos Fijos** y la suma total de **Gastos Fijos + Variables** sobre tu flujo mensual:
    - 🟢 **EXCELENTE:** Gastos fijos menores al **50%** o Gastos fijos + variables menores al **70%**.
    - 🟡 **ACEPTABLE:** Gastos fijos entre **50%** y **60%** o Gastos fijos + variables entre **70%** y **80%**.
    - 🔴 **CRÍTICO:** Gastos fijos mayores al **60%** o Gastos fijos + variables mayores al **80%**.
    """)

st.divider()

st.header("1. Ingresa tus salidas mensuales")

# Entradas manuales
col1, col2 = st.columns(2)
with col1:
    gastos_fijos = st.number_input("Gastos Fijos (\$)", min_value=0.0, value=650.0, step=50.0)
    gastos_variables = st.number_input("Gastos Variables (\$)", min_value=0.0, value=200.0, step=50.0)
with col2:
    ahorro = st.number_input("Ahorro (\$)", min_value=0.0, value=50.0, step=10.0)
    fondo_reserva = st.number_input("Fondo/Inversión (\$)", min_value=0.0, value=50.0, step=10.0)

if st.button("Hacer Diagnóstico", type="primary"):
    
    # El ingreso actual implícito es simplemente la suma de todo lo que el usuario distribuye hoy
    ingreso_actual_implicito = gastos_fijos + gastos_variables + ahorro + fondo_reserva
    
    if ingreso_actual_implicito == 0:
        st.error("Debes ingresar montos mayores a \$0 para calcular tu diagnóstico.")
    elif gastos_fijos == 0:
        st.error("Debes registrar tus Gastos Fijos para poder evaluar tu estatus.")
    else:
        st.divider()
        st.header("2. Resultados del Diagnóstico Actual")
        
        st.info(f"💡 Sumando tus gastos y asignaciones actuales, estimamos que tu nivel de ingresos (o flujo de caja) mensual es de **\$ {ingreso_actual_implicito:,.2f}**.")
        
        # Análisis del Estatus (Evaluando Fijos y Fijos + Variables)
        pct_fijos = (gastos_fijos / ingreso_actual_implicito) * 100
        pct_fijos_vars = ((gastos_fijos + gastos_variables) / ingreso_actual_implicito) * 100
        
        # Lógica en cascada: Prioriza la detección de riesgo
        if pct_fijos > 60 or pct_fijos_vars > 80:
            estado = "CRÍTICO"
            color = "#dc3545" # Rojo
            mensaje = f"Tus Gastos Fijos son el **{pct_fijos:.1f}%** y la suma con tus variables alcanza el **{pct_fijos_vars:.1f}%**. Has superado los límites seguros (60% y 80% respectivamente)."
        elif (50 <= pct_fijos <= 60) or (70 <= pct_fijos_vars <= 80):
            estado = "ACEPTABLE"
            color = "#ffc107" # Amarillo
            mensaje = f"Tus Gastos Fijos son el **{pct_fijos:.1f}%** y la suma con tus variables es el **{pct_fijos_vars:.1f}%**. Te mantienes dentro de los rangos saludables."
        else:
            estado = "EXCELENTE"
            color = "#28a745" # Verde
            mensaje = f"Tus Gastos Fijos son el **{pct_fijos:.1f}%** y la suma con tus variables es el **{pct_fijos_vars:.1f}%**. ¡Tienes una estructura muy ligera y óptima!"

        st.markdown(mensaje)
        st.markdown(f"Estatus actual de tu estructura: <strong style='color:{color}; font-size: 1.3em;'>{estado}</strong>", unsafe_allow_html=True)

        st.divider()
        
        # --- DESGLOSE DE FLUJO DE CAJA ---
        st.subheader("📊 Desglose de tu Flujo de Caja")
        st.write("Así se distribuye actualmente tu dinero en base a tus salidas totales:")
        
        pct_vars = (gastos_variables / ingreso_actual_implicito) * 100
        pct_ahorro = (ahorro / ingreso_actual_implicito) * 100
        pct_fondo = (fondo_reserva / ingreso_actual_implicito) * 100
        
        df_desglose = pd.DataFrame({
            "Categoría": ["Gastos Fijos", "Gastos Variables", "Ahorro", "Fondo/Inversión"],
            "Monto": [gastos_fijos, gastos_variables, ahorro, fondo_reserva],
            "Peso en tu Flujo (%)": [f"{pct_fijos:.1f}%", f"{pct_vars:.1f}%", f"{pct_ahorro:.1f}%", f"{pct_fondo:.1f}%"]
        })
        
        # Formateo de moneda para la columna de Monto
        df_desglose["Monto"] = df_desglose["Monto"].apply(lambda x: f"$ {x:,.2f}")
        
        st.table(df_desglose)
