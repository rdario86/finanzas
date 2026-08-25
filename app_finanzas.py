import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diagnóstico Financiero", page_icon="📊", layout="wide")

# Encabezado personalizado
st.title("Diagnóstico Financiero 📊")
st.markdown("#### Panel de Control - Rubén Núñez")
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
        
        # Cálculo de balance
        balance = ingresos - total_egresos
        
        if balance > 0:
            st.success(f"**EXCEDENTE:** Tienes un saldo a favor de **\$ {balance:,.2f}**")
        elif balance < 0:
            deuda_estimada = abs(balance)
            st.error(f"**DÉFICIT DETECTADO:** Tus salidas superan tus ingresos. Te faltan **\$ {deuda_estimada:,.2f}**, lo que indica que estás asumiendo **DEUDAS** para poder cubrir tus compromisos.")
        else:
            st.info(f"**PUNTO DE EQUILIBRIO:** Tus ingresos cubren exactamente tus salidas (\$ 0.00).")

        # Estatus de las finanzas
        total_fijos_vars = gastos_fijos + gastos_variables
        pct_fijos_vars = (total_fijos_vars / ingresos) * 100
        
        if balance < 0:
            estado = "CRÍTICO"
            color = "#dc3545"
            mensaje_pct = f"Tus gastos fijos y variables representan el **{pct_fijos_vars:.1f}%** de tus ingresos, pero asumes deudas."
        elif pct_fijos_vars < 70:
            estado = "EXCELENTE"
            color = "#28a745"
            mensaje_pct = f"Tus gastos fijos y variables representan el **{pct_fijos_vars:.1f}%** de tus ingresos."
        elif pct_fijos_vars <= 80:
            estado = "ACEPTABLE"
            color = "#ffc107"
            mensaje_pct = f"Tus gastos fijos y variables representan el **{pct_fijos_vars:.1f}%** de tus ingresos."
        else:
            estado = "CRÍTICO"
            color = "#dc3545"
            mensaje_pct = f"Tus gastos fijos y variables representan el **{pct_fijos_vars:.1f}%** de tus ingresos."

        st.markdown(mensaje_pct)
        st.markdown(f"Estado de tus finanzas: <strong style='color:{color}; font-size: 1.2em;'>{estado}</strong>", unsafe_allow_html=True)

        st.divider()

        # ==========================================================
        # MÓDULO: PLAN DE RESCATE (Solo si hay déficit)
        # ==========================================================
        if balance < 0:
            st.subheader("🚨 Plan de Rescate Inmediato")
            st.markdown("Antes de proyectar metas a futuro, la **primera regla financiera** es frenar la deuda. Para lograrlo usando tus ingresos actuales, tu presupuesto debe reestructurarse bajo la regla de emergencia **60/20/20** (suspendiendo temporalmente el ahorro y la inversión):")
            
            fijos_rescate = ingresos * 0.60
            var_rescate = ingresos * 0.20
            deudas_rescate = ingresos * 0.20
            
            df_rescate = pd.DataFrame({
                "Categoría": ["Gastos Fijos (60%)", "Gastos Variables (20%)", "Pago de Deudas (20%)"],
                "Presupuesto de Emergencia": [fijos_rescate, var_rescate, deudas_rescate]
            })
            df_rescate["Presupuesto de Emergencia"] = df_rescate["Presupuesto de Emergencia"].apply(lambda x: f"$ {x:,.2f}")
            st.table(df_rescate)
            
            if gastos_fijos > fijos_rescate:
                st.error(f"⚠️ **ALERTA CRÍTICA:** Tus Gastos Fijos actuales (**\$ {gastos_fijos:,.2f}**) superan el límite del 60% (**\$ {fijos_rescate:,.2f}**) permitido en este plan de emergencia. Tienes un problema estructural: debes reducir drásticamente tu estilo de vida fijo o tu única salida será inyectar capital (ver opciones abajo).")
            else:
                st.success("✅ Si logras ajustar tus salidas a estos montos exactos, lograrás frenar el endeudamiento e ir saldando tus compromisos. Luego de estabilizarte, evalúa los siguientes planes para aumentar ingresos.")
                
            st.divider()

        # ==========================================================
        # FUNCIÓN DE PLAN DE ACCIÓN ÚNICO
        # ==========================================================
        def mostrar_plan_accion():
            st.subheader("💡 Plan de Acción")
            col_a, col_b = st.columns(2)
            
            # --- OPCIÓN A: ACEPTABLE (Target 80%) ---
            with col_a:
                target_pct_a = 0.80
                ingreso_req_a = total_fijos_vars / target_pct_a if target_pct_a > 0 else 0
                st.markdown("**Opción A: Nivel ACEPTABLE**")
                st.write(f"Para que tus gastos actuales sean el 80%, debes ganar **\$ {ingreso_req_a:,.2f}**:")
                
                ahorro_a = ingreso_req_a * 0.10
                fondo_a = ingreso_req_a * 0.10
                pct_fijos_a = (gastos_fijos / ingreso_req_a) * 100 if ingreso_req_a > 0 else 0
                pct_vars_a = (gastos_variables / ingreso_req_a) * 100 if ingreso_req_a > 0 else 0
                excedente_a = ingreso_req_a - (gastos_fijos + gastos_variables + ahorro_a + fondo_a)
                
                cats_a = [f"Fijos ({pct_fijos_a:.1f}%)", f"Variables ({pct_vars_a:.1f}%)", "Ahorro (10%)", "Inversión (10%)"]
                montos_a = [gastos_fijos, gastos_variables, ahorro_a, fondo_a]
                
                if excedente_a > 0.01:
                    cats_a.append(f"Excedente ({(excedente_a/ingreso_req_a)*100:.1f}%)")
                    montos_a.append(excedente_a)
                    
                df_a = pd.DataFrame({"Categoría": cats_a, "Presupuesto": montos_a})
                df_a["Presupuesto"] = df_a["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                st.table(df_a)

            # --- OPCIÓN B: EXCELENTE (Target 70%) ---
            with col_b:
                target_pct_b = 0.70
                ingreso_req_b = total_fijos_vars / target_pct_b if target_pct_b > 0 else 0
                st.markdown("**Opción B: Nivel EXCELENTE**")
                st.write(f"Para que tus gastos actuales sean el 70%, debes ganar **\$ {ingreso_req_b:,.2f}**:")
                
                ahorro_b = ingreso_req_b * 0.10
                fondo_b = ingreso_req_b * 0.10
                pct_fijos_b = (gastos_fijos / ingreso_req_b) * 100 if ingreso_req_b > 0 else 0
                pct_vars_b = (gastos_variables / ingreso_req_b) * 100 if ingreso_req_b > 0 else 0
                excedente_b = ingreso_req_b - (gastos_fijos + gastos_variables + ahorro_b + fondo_b)
                
                cats_b = [f"Fijos ({pct_fijos_b:.1f}%)", f"Variables ({pct_vars_b:.1f}%)", "Ahorro (10%)", "Inversión (10%)"]
                montos_b = [gastos_fijos, gastos_variables, ahorro_b, fondo_b]
                
                if excedente_b > 0.01:
                    cats_b.append(f"Excedente Libre ({(excedente_b/ingreso_req_b)*100:.1f}%)")
                    montos_b.append(excedente_b)
                    
                df_b = pd.DataFrame({"Categoría": cats_b, "Presupuesto": montos_b})
                df_b["Presupuesto"] = df_b["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                st.table(df_b)

        # Disparador de recomendaciones
        if estado == "CRÍTICO":
            if not (balance < 0): 
                st.warning("⚠️ **Estrategia sugerida:** Dado tu estatus, la prioridad es inyectar capital para ajustar tus porcentajes. Aquí tienes los números objetivo:")
            mostrar_plan_accion()
            
        elif estado == "ACEPTABLE":
            mostrar_plan_accion()
