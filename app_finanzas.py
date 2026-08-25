import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diagnóstico Financiero", page_icon="📊", layout="centered")

# Encabezado personalizado
st.title("Diagnóstico Financiero 📊")
st.markdown("#### Panel de Control - Rubén Núñez")
st.markdown("Evalúa tu salud financiera según el peso de tus gastos fijos y descubre tu meta de ingresos ideal.")

# Nueva Leyenda del Diagnóstico (Regla de Fijos)
with st.expander("ℹ️ Nueva Regla: ¿Cómo se evalúa el estatus financiero?"):
    st.markdown("""
    El estado de tus finanzas se determina ahora **exclusivamente** por el porcentaje que representan tus **Gastos Fijos** sobre tus **Ingresos Totales**:
    - 🟢 **EXCELENTE:** Gastos fijos son menores al **50%**.
    - 🟡 **ACEPTABLE:** Gastos fijos entre el **50%** y el **60%**.
    - 🔴 **CRÍTICO:** Gastos fijos mayores al **60%** (o si presentas déficit mensual).
    
    *La meta universal recomendada para estructurar tu presupuesto será el método **60/20/10/10**.*
    """)

st.divider()

st.header("1. Ingresa tus datos mensuales")

# Entradas manuales (sin sliders, como prefieres)
col1, col2 = st.columns(2)
with col1:
    ingresos = st.number_input("Ingresos Totales (\$)", min_value=0.0, value=1000.0, step=100.0)
    gastos_fijos = st.number_input("Gastos Fijos (\$)", min_value=0.0, value=650.0, step=50.0)
    gastos_variables = st.number_input("Gastos Variables (\$)", min_value=0.0, value=200.0, step=50.0)
with col2:
    ahorro = st.number_input("Ahorro (\$)", min_value=0.0, value=50.0, step=10.0)
    fondo_reserva = st.number_input("Fondo/Inversión (\$)", min_value=0.0, value=50.0, step=10.0)

if st.button("Hacer Diagnóstico", type="primary"):
    if ingresos == 0:
        st.error("Los ingresos deben ser mayores a \$0 para poder evaluar los porcentajes.")
    elif gastos_fijos == 0:
        st.error("Debes registrar tus Gastos Fijos para poder proyectar tu ingreso ideal.")
    else:
        st.divider()
        st.header("2. Resultados del Diagnóstico")
        
        # 1. Análisis de Liquidez Actual
        total_egresos = gastos_fijos + gastos_variables + ahorro + fondo_reserva
        balance = ingresos - total_egresos
        
        if balance > 0:
            st.success(f"**EXCEDENTE:** Tienes un saldo libre a favor de **\$ {balance:,.2f}**")
        elif balance < 0:
            st.error(f"**DÉFICIT DETECTADO:** Te faltan **\$ {abs(balance):,.2f}** para cubrir tus salidas, lo que indica endeudamiento.")
        else:
            st.info(f"**PUNTO DE EQUILIBRIO:** Tus ingresos cubren tus salidas de forma exacta (\$ 0.00).")

        # 2. Análisis del Estatus (Basado SOLO en Gastos Fijos)
        pct_fijos = (gastos_fijos / ingresos) * 100
        
        if balance < 0:
            estado = "CRÍTICO"
            color = "#dc3545" # Rojo
            mensaje = f"Tus Gastos Fijos son el **{pct_fijos:.1f}%**, pero presentas déficit. La deuda te coloca en estado crítico."
        elif pct_fijos > 60:
            estado = "CRÍTICO"
            color = "#dc3545" # Rojo
            mensaje = f"Tus Gastos Fijos representan el **{pct_fijos:.1f}%** de tus ingresos (Superan el límite seguro del 60%)."
        elif pct_fijos >= 50:
            estado = "ACEPTABLE"
            color = "#ffc107" # Amarillo
            mensaje = f"Tus Gastos Fijos representan el **{pct_fijos:.1f}%** de tus ingresos (Están dentro del rango 50%-60%)."
        else:
            estado = "EXCELENTE"
            color = "#28a745" # Verde
            mensaje = f"Tus Gastos Fijos representan el **{pct_fijos:.1f}%** de tus ingresos (¡Por debajo del 50%!)."

        st.markdown(mensaje)
        st.markdown(f"Estatus de tu estructura: <strong style='color:{color}; font-size: 1.3em;'>{estado}</strong>", unsafe_allow_html=True)

        st.divider()
        
        # 3. Recomendación de Ingreso y Distribución
        st.header("3. Plan de Acción: Tu Ingreso Ideal")
        
        # Matemáticamente: Si los Fijos deben ser el 60%, el Ingreso Ideal = Fijos / 0.60
        ingreso_ideal = gastos_fijos / 0.60
        
        st.markdown(f"Tomando como base tus Gastos Fijos inamovibles (**\$ {gastos_fijos:,.2f}**), para que estos representen exactamente el 60% de tu pastel financiero, necesitas establecer una meta de ingresos de:")
        st.markdown(f"<h2 style='color:#0056b3; text-align: center;'>$ {ingreso_ideal:,.2f}</h2>", unsafe_allow_html=True)
        
        st.write("Alcanzando este nivel de ingresos, tu distribución perfecta bajo la regla **60/20/10/10** sería la siguiente:")
        
        # Cálculo de la distribución sobre el Ingreso Ideal
        var_ideal = ingreso_ideal * 0.20
        ahorro_ideal = ingreso_ideal * 0.10
        fondo_ideal = ingreso_ideal * 0.10
        
        df_ideal = pd.DataFrame({
            "Categoría": ["Gastos Fijos (60%)", "Gastos Variables (20%)", "Ahorro (10%)", "Fondo/Inversión (10%)"],
            "Presupuesto Meta": [gastos_fijos, var_ideal, ahorro_ideal, fondo_ideal]
        })
        df_ideal["Presupuesto Meta"] = df_ideal["Presupuesto Meta"].apply(lambda x: f"$ {x:,.2f}")
        
        st.table(df_ideal)
        
        # Mensaje de cierre comparativo
        diferencia = ingreso_ideal - ingresos
        if diferencia > 0:
            st.warning(f"💡 **Estrategia:** Te faltan **\$ {diferencia:,.2f}** mensuales para llegar a este balance. Concéntrate en aumentar tu facturación sin subir tus gastos fijos actuales.")
        elif diferencia < 0:
            st.success(f"🌟 **¡Estás por encima de la meta!** Tienes un excedente estructural de **\$ {abs(diferencia):,.2f}** respecto al requerimiento mínimo de tus Fijos. Úsalo para potenciar tu fondo de inversión.")
        else:
            st.success("🎯 Tus ingresos actuales calzan perfectamente con la estructura ideal.")
