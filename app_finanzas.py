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

        # Función de planes de acción
        def mostrar_planes(nivel, target_pct):
            st.subheader(f"💡 Plan de Acción para lograr estado: {nivel}")
            
            # REGLA PARA EXCELENTE: Solo mostrar Aumentar Ingresos
            if nivel == "EXCELENTE":
                ingreso_requerido = total_fijos_vars / target_pct if target_pct > 0 else 0
                st.markdown(f"**Recomendación Única: Aumentar Ingresos**")
                st.write(f"Para llegar a EXCELENTE manteniendo tus gastos iniciales, debes elevar tus ingresos a **\$ {ingreso_requerido:,.2f}**:")
                
                ahorro_sim = ingreso_requerido * 0.10
                fondo_sim = ingreso_requerido * 0.10
                
                pct_fijos_real = (gastos_fijos / ingreso_requerido) * 100 if ingreso_requerido > 0 else 0
                pct_vars_real = (gastos_variables / ingreso_requerido) * 100 if ingreso_requerido > 0 else 0
                
                excedente_sim = ingreso_requerido - (gastos_fijos + gastos_variables + ahorro_sim + fondo_sim)
                
                cats = [f"Gastos Fijos ({pct_fijos_real:.1f}%)", f"Gastos Vars ({pct_vars_real:.1f}%)", "Ahorro (10%)", "Fondo/Inv. (10%)"]
                montos = [gastos_fijos, gastos_variables, ahorro_sim, fondo_sim]
                
                if excedente_sim > 0.01:
                    pct_excedente = (excedente_sim / ingreso_requerido) * 100
                    cats.append(f"Excedente Libre ({pct_excedente:.1f}%)")
                    montos.append(excedente_sim)
                
                df_excelente = pd.DataFrame({"Categoría": cats, "Presupuesto": montos})
                df_excelente["Presupuesto"] = df_excelente["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                st.table(df_excelente)
                
            # REGLA PARA ACEPTABLE: Mostrar ambas opciones
            else:
                col_a, col_b = st.columns(2)
                
                # --- OPCIÓN A: REESTRUCTURAR GASTOS (BLOQUEANDO GASTOS FIJOS) ---
                with col_a:
                    st.markdown(f"**Opción A: Reestructurar Gastos**")
                    st.write(f"Manteniendo tus ingresos de **\$ {ingresos:,.2f}** y tus Gastos Fijos bloqueados, tu distribución debe ser:")
                    
                    # 1. Los gastos fijos se mantienen exactamente igual
                    fijos_sim_a = gastos_fijos
                    
                    # 2. Se aparta el 10% para ahorro y 10% para fondo del ingreso actual
                    ahorro_sim_a = ingresos * 0.10
                    fondo_sim_a = ingresos * 0.10
                    
                    # 3. Los gastos variables asumen el recorte (lo que sobra del ingreso)
                    variables_sim_a = ingresos - fijos_sim_a - ahorro_sim_a - fondo_sim_a
                    
                    if variables_sim_a < 0:
                        st.error("⚠️ Tus Gastos Fijos actuales son tan altos que matemáticamente no queda dinero para gastos variables. Necesitas aumentar ingresos (Opción B).")
                    
                    pct_fijos_a = (fijos_sim_a / ingresos) * 100 if ingresos > 0 else 0
                    pct_vars_a = (variables_sim_a / ingresos) * 100 if ingresos > 0 else 0
                    
                    df_opcion_a = pd.DataFrame({
                        "Categoría": [f"Gastos Fijos ({pct_fijos_a:.1f}%)", f"Gastos Variables Ajustados ({pct_vars_a:.1f}%)", "Ahorro (10.0%)", "Fondo/Inversión (10.0%)"],
                        "Presupuesto": [fijos_sim_a, variables_sim_a, ahorro_sim_a, fondo_sim_a]
                    })
                    df_opcion_a["Presupuesto"] = df_opcion_a["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                    st.table(df_opcion_a)
                    
                    # Alertas de deuda integradas en la Opción A
                    if balance < 0:
                        st.info("ℹ️ **Nota:** Como presentas déficit y deudas, el 20% destinado a ahorro e inversión debe ser usado exclusivamente para pagar deudas hasta saldar las mismas.")
                        
                        if abs(balance) > (ingresos * 0.20):
                            st.warning("⚠️ **Alerta:** Tus deudas mensuales exceden el 20% de tus ingresos. Debes recortar radicalmente tus gastos variables o buscar más ingresos.")

                # --- OPCIÓN B: AUMENTAR INGRESOS ---
                with col_b:
                    ingreso_requerido = total_fijos_vars / target_pct if target_pct > 0 else 0
                    st.markdown(f"**Opción B: Aumentar Ingresos**")
                    st.write(f"Manteniendo tus gastos iniciales (fijos y variables), debes elevar tus ingresos a **\$ {ingreso_requerido:,.2f}**:")
                    
                    ahorro_sim = ingreso_requerido * 0.10
                    fondo_sim = ingreso_requerido * 0.10
                    
                    pct_fijos_real = (gastos_fijos / ingreso_requerido) * 100 if ingreso_requerido > 0 else 0
                    pct_vars_real = (gastos_variables / ingreso_requerido) * 100 if ingreso_requerido > 0 else 0
                    
                    excedente_sim = ingreso_requerido - (gastos_fijos + gastos_variables + ahorro_sim + fondo_sim)
                    
                    cats_b = [f"Gastos Fijos ({pct_fijos_real:.1f}%)", f"Gastos Vars ({pct_vars_real:.1f}%)", "Ahorro (10%)", "Fondo/Inv. (10%)"]
                    montos_b = [gastos_fijos, gastos_variables, ahorro_sim, fondo_sim]
                    
                    if excedente_sim > 0.01:
                        pct_excedente = (excedente_sim / ingreso_requerido) * 100
                        cats_b.append(f"Excedente Libre ({pct_excedente:.1f}%)")
                        montos_b.append(excedente_sim)
                    
                    df_opcion_b = pd.DataFrame({"Categoría": cats_b, "Presupuesto": montos_b})
                    df_opcion_b["Presupuesto"] = df_opcion_b["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                    st.table(df_opcion_b)

        # Disparador de recomendaciones
        if estado == "CRÍTICO":
            mostrar_planes("ACEPTABLE", 0.80)
            st.divider()
            mostrar_planes("EXCELENTE", 0.70)
            
        elif estado == "ACEPTABLE":
            mostrar_planes("EXCELENTE", 0.70)
