import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diagnóstico Financiero", page_icon="📊", layout="centered")

# Encabezado personalizado
st.title("Diagnóstico Financiero 📊")
st.markdown("Determina tu estatus financiero y proyecta tus metas de ingresos en USD (\$).")

# Nueva Leyenda del Diagnóstico
with st.expander("ℹ️ Leyenda: ¿Cómo se evalúa el estatus financiero?"):
    st.markdown("""
    El estado de tus finanzas se determina por el porcentaje que representan tus **Gastos Fijos y Variables** sobre tus **Ingresos Totales**:
    - 🟢 **EXCELENTE:** Gastos fijos y variables son menores al **70%**.
    - 🟡 **ACEPTABLE:** Gastos fijos y variables entre el **70%** y **80%**.
    - 🔴 **CRÍTICO:** Gastos fijos y variables mayores al **80%** (O si presentas déficit y asumes deudas).
    """)

st.divider()

st.header("1. Ingresa tus datos mensuales")

col1, col2 = st.columns(2)
with col1:
    ingresos = st.number_input("Ingresos Totales (\$)", min_value=0.0, value=1000.0, step=100.0)
    gastos_fijos = st.number_input("Gastos Fijos (\$)", min_value=0.0, value=650.0, step=50.0)
    gastos_variables = st.number_input("Gastos Variables (\$)", min_value=0.0, value=200.0, step=50.0)
with col2:
    ahorro = st.number_input("Ahorro (\$)", min_value=0.0, value=50.0, step=10.0)
    fondo_reserva = st.number_input("Fondo de Reserva (\$)", min_value=0.0, value=50.0, step=10.0)

if st.button("Hacer Diagnóstico", type="primary"):
    
    if ingresos == 0:
        st.error("Los ingresos deben ser mayores a \$0 para calcular los indicadores.")
    else:
        st.divider()
        st.header("2. Resultados del Diagnóstico")
        
        # Sumatoria de todas las salidas
        total_egresos = gastos_fijos + gastos_variables + ahorro + fondo_reserva
        
        # Cálculo de balance (Excedente o Déficit)
        balance = ingresos - total_egresos
        
        if balance > 0:
            st.success(f"**EXCEDENTE:** Tienes un saldo a favor de **\$ {balance:,.2f}**")
        elif balance < 0:
            deuda_estimada = abs(balance)
            st.error(f"**DÉFICIT DETECTADO:** Tus salidas superan tus ingresos. Te faltan **\$ {deuda_estimada:,.2f}**, lo que indica que estás asumiendo **DEUDAS** para poder cubrir tus compromisos.")
        else:
            st.info(f"**PUNTO DE EQUILIBRIO:** Tus ingresos cubren exactamente tus salidas (\$ 0.00).")

        # Estatus de las finanzas (Evaluando Fijos + Variables juntos)
        total_fijos_vars = gastos_fijos + gastos_variables
        pct_fijos_vars = (total_fijos_vars / ingresos) * 100
        
        # LÓGICA DE ESTATUS: El déficit fuerza el estado a CRÍTICO
        if balance < 0:
            estado = "CRÍTICO"
            color = "#dc3545" # Rojo
            mensaje_pct = f"Tus gastos fijos y variables representan el **{pct_fijos_vars:.1f}%** de tus ingresos, lo que te coloca en estado de riesgo."
        elif pct_fijos_vars < 70:
            estado = "EXCELENTE"
            color = "#28a745" # Verde
            mensaje_pct = f"Tus gastos fijos y variables representan el **{pct_fijos_vars:.1f}%** de tus ingresos."
        elif pct_fijos_vars <= 80:
            estado = "ACEPTABLE"
            color = "#ffc107" # Amarillo
            mensaje_pct = f"Tus gastos fijos y variables representan el **{pct_fijos_vars:.1f}%** de tus ingresos."
        else:
            estado = "CRÍTICO"
            color = "#dc3545" # Rojo
            mensaje_pct = f"Tus gastos fijos y variables representan el **{pct_fijos_vars:.1f}%** de tus ingresos."

        st.markdown(mensaje_pct)
        st.markdown(f"Estado de tus finanzas: <strong style='color:{color}; font-size: 1.2em;'>{estado}</strong>", unsafe_allow_html=True)

        st.divider()

        # Función para simular el presupuesto ideal con la distribución 60/20/10/10
        def mostrar_simulacion(ingreso_req, nivel):
            st.subheader(f"💡 Plan de Acción: {nivel}")
            
            if "Reestructuración" in nivel:
                st.markdown(f"Distribuyendo tus ingresos actuales de **\$ {ingreso_req:,.2f}** bajo la regla recomendada, tu estructura ideal sería:")
            else:
                st.markdown(f"Para lograr el estado {nivel} (cubriendo tus gastos base actuales), tus ingresos deben ser de al menos **\$ {ingreso_req:,.2f}**.")
                st.write("Con ese nuevo nivel de ingresos, tu distribución ideal sería:")
            
            # Cálculo basado estrictamente en la regla 60/20/10/10
            fijos_sim = ingreso_req * 0.60
            variables_sim = ingreso_req * 0.20
            ahorro_sim = ingreso_req * 0.10
            fondo_sim = ingreso_req * 0.10
            
            data = {
                "Categoría": [
                    "Gastos Fijos (60.0%)", 
                    "Gastos Variables (20.0%)", 
                    "Ahorro (10.0%)", 
                    "Fondo/Inversión (10.0%)"
                ],
                "Presupuesto Sugerido": [
                    fijos_sim,
                    variables_sim,
                    ahorro_sim,
                    fondo_sim
                ]
            }
                
            df_simulacion = pd.DataFrame(data)
            
            # Formateo de moneda
            df_simulacion["Presupuesto Sugerido"] = df_simulacion["Presupuesto Sugerido"].apply(lambda x: f"$ {x:,.2f}")
            
            st.table(df_simulacion)

        # Lógica de proyecciones según el estado actual
        if estado == "CRÍTICO":
            if balance < 0 and pct_fijos_vars < 70:
                st.warning("⚠️ **Análisis Especial:** Tus gastos base (fijos + variables) son menores al 70% (¡excelente!), pero asumes deudas porque te excedes en ahorros o fondos. No necesitas ganar más, necesitas reestructurar tus salidas.")
                mostrar_simulacion(ingresos, "Reestructuración (Ingreso Actual)")
                
            elif balance < 0 and pct_fijos_vars <= 80:
                st.warning("⚠️ **Análisis Especial:** Tus gastos base (fijos + variables) son aceptables (menores al 80%), pero asumes deudas por asignar de más al ahorro/fondos. Puedes reestructurar tus gastos actuales, o apuntar al estado EXCELENTE incrementando tus ingresos.")
                mostrar_simulacion(ingresos, "Reestructuración (Ingreso Actual)")
                
                ingreso_excelente = total_fijos_vars / 0.70 
                mostrar_simulacion(ingreso_excelente, "EXCELENTE")
                
            else:
                ingreso_aceptable = total_fijos_vars / 0.80
                mostrar_simulacion(ingreso_aceptable, "ACEPTABLE")
                
                ingreso_excelente = total_fijos_vars / 0.70 
                mostrar_simulacion(ingreso_excelente, "EXCELENTE")

        elif estado == "ACEPTABLE":
            ingreso_excelente = total_fijos_vars / 0.70
            mostrar_simulacion(ingreso_excelente, "EXCELENTE")
