import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diagnóstico Financiero", page_icon="📊", layout="centered")

# Encabezado personalizado
st.title("Diagnóstico Financiero 📊")
st.markdown("#### Panel de Control")
st.markdown("Determina tu estatus financiero y proyecta tus metas de ingresos en USD (\$).")

# Nueva Leyenda del Diagnóstico
with st.expander("ℹ️ Leyenda: ¿Cómo se evalúa el estatus financiero?"):
    st.markdown("""
    El estado de tus finanzas se determina por el porcentaje que representan tus **Gastos Fijos** sobre tus **Ingresos Totales**:
    - 🟢 **EXCELENTE:** Gastos fijos menores al **50%**.
    - 🟡 **ACEPTABLE:** Gastos fijos entre el **50%** y **60%**.
    - 🔴 **CRÍTICO:** Gastos fijos mayores al **60%**.
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
        
        # Cálculo de balance (Excedente o Déficit)
        total_egresos = gastos_fijos + gastos_variables + ahorro + fondo_reserva
        balance = ingresos - total_egresos
        
        if balance > 0:
            st.success(f"**EXCEDENTE:** Tienes un saldo a favor de **\$ {balance:,.2f}**")
        elif balance < 0:
            st.error(f"**DÉFICIT:** Te faltan **\$ {abs(balance):,.2f}** para cubrir tus compromisos.")
        else:
            st.info(f"**PUNTO DE EQUILIBRIO:** Tus ingresos cubren exactamente tus salidas (\$ 0.00).")

        # Estatus de las finanzas
        pct_fijos = (gastos_fijos / ingresos) * 100
        
        if pct_fijos < 50:
            estado = "EXCELENTE"
            color = "#28a745" # Verde
        elif pct_fijos <= 60:
            estado = "ACEPTABLE"
            color = "#ffc107" # Amarillo
        else:
            estado = "CRÍTICO"
            color = "#dc3545" # Rojo

        st.markdown(f"Tus gastos fijos representan el **{pct_fijos:.1f}%** de tus ingresos.")
        st.markdown(f"Estado de tus finanzas: <strong style='color:{color}; font-size: 1.2em;'>{estado}</strong>", unsafe_allow_html=True)

        st.divider()

        # Función para simular el presupuesto ideal
        def mostrar_simulacion(ingreso_req, nivel):
            st.subheader(f"💡 Plan de Acción para estado: {nivel}")
            
            st.markdown(f"Para lograr este nivel (manteniendo tus gastos fijos en **\$ {gastos_fijos:,.2f}**), tus ingresos deben ser de al menos **\$ {ingreso_req:,.2f}**.")
            st.write("Con ese nuevo nivel de ingresos, tu distribución automática ideal sería:")
            
            # Bloqueo del monto de gastos fijos
            fijos_sim = gastos_fijos
            
            # Cálculo del resto basado en la regla 20/10/10 sobre el NUEVO ingreso
            variables_sim = ingreso_req * 0.20
            ahorro_sim = ingreso_req * 0.10
            fondo_sim = ingreso_req * 0.10
            
            # Cálculo de excedente si se llega a excelente (ya que fijos serán <= 50%)
            excedente_sim = ingreso_req - (fijos_sim + variables_sim + ahorro_sim + fondo_sim)
            pct_fijos_real = (fijos_sim / ingreso_req) * 100
            
            data = {
                "Categoría": [
                    f"Gastos Fijos ({pct_fijos_real:.1f}%)", 
                    "Gastos Variables (20%)", 
                    "Ahorro (10%)", 
                    "Fondo/Inversión (10%)"
                ],
                "Presupuesto Sugerido": [
                    fijos_sim,
                    variables_sim,
                    ahorro_sim,
                    fondo_sim
                ]
            }
            
            # Agrega el excedente a la tabla si existe
            if excedente_sim > 0.01:
                pct_excedente = (excedente_sim / ingreso_req) * 100
                data["Categoría"].append(f"Excedente Libre ({pct_excedente:.1f}%)")
                data["Presupuesto Sugerido"].append(excedente_sim)
                
            df_simulacion = pd.DataFrame(data)
            
            # Formateo de moneda
            df_simulacion["Presupuesto Sugerido"] = df_simulacion["Presupuesto Sugerido"].apply(lambda x: f"$ {x:,.2f}")
            
            st.table(df_simulacion)

        # Lógica de proyecciones según el estado actual
        if estado == "CRÍTICO":
            ingreso_aceptable = gastos_fijos / 0.60
            mostrar_simulacion(ingreso_aceptable, "ACEPTABLE")
            
            ingreso_excelente = gastos_fijos / 0.50 
            mostrar_simulacion(ingreso_excelente, "EXCELENTE")

        elif estado == "ACEPTABLE":
            ingreso_excelente = gastos_fijos / 0.50
            mostrar_simulacion(ingreso_excelente, "EXCELENTE")
