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
        # NUEVO MÓDULO: PLAN DE RESCATE (Solo si hay déficit)
        # ==========================================================
        if balance < 0:
            st.subheader("🚨 Plan de Rescate Inmediato")
            st.markdown("Antes de proyectar metas a futuro, la **primera regla financiera** es frenar la deuda. Para lograrlo usando tus ingresos actuales, debes ejecutar un recorte estricto en el siguiente orden de prioridad:")
            
            deuda_actual = abs(balance)
            var_rec = gastos_variables
            ahorro_rec = ahorro
            fondo_rec = fondo_reserva
            
            # 1. Recortar Gastos Variables
            recorte_var = min(deuda_actual, var_rec)
            var_rec -= recorte_var
            deuda_actual -= recorte_var
            
            # 2. Recortar Ahorro (si aún hay deuda)
            recorte_ahorro = min(deuda_actual, ahorro_rec)
            ahorro_rec -= recorte_ahorro
            deuda_actual -= recorte_ahorro
            
            # 3. Recortar Fondo (si aún hay deuda)
            recorte_fondo = min(deuda_actual, fondo_rec)
            fondo_rec -= recorte_fondo
            deuda_actual -= recorte_fondo
            
            df_rescate = pd.DataFrame({
                "Categoría (Orden de Recorte)": ["Gastos Fijos (Intocables)", "Gastos Variables", "Ahorro", "Fondo de Reserva"],
                "Presupuesto de Emergencia": [gastos_fijos, var_rec, ahorro_rec, fondo_rec]
            })
            df_rescate["Presupuesto de Emergencia"] = df_rescate["Presupuesto de Emergencia"].apply(lambda x: f"$ {x:,.2f}")
            st.table(df_rescate)
            
            if deuda_actual > 0:
                st.error(f"⚠️ **ALERTA CRÍTICA:** Incluso recortando a **$0** tus gastos variables, ahorros y fondo de reserva, tus Gastos Fijos (**\$ {gastos_fijos:,.2f}**) superan tus Ingresos Totales. Matemáticamente sigues en déficit por **\$ {deuda_actual:,.2f}**. Tu única salida real es inyectar capital.")
            else:
                st.success("✅ Ajustando tus salidas a estos montos exactos de emergencia, lograrás empatar tus egresos con el total de tus ingresos actuales (**\$ {:.2f}**), frenando el endeudamiento. Luego de estabilizarte, evalúa los siguientes planes para aumentar ingresos.".format(ingresos))
                
            st.divider()

        # ==========================================================
        # FUNCIÓN DE PLANES DE ACCIÓN (Proyecciones ACEPTABLE / EXCELENTE)
        # ==========================================================
        def mostrar_planes(nivel, target_pct, es_critico=False):
            st.subheader(f"💡 Plan de Acción para lograr estado: {nivel}")

            # REGLA PARA EXCELENTE
            if nivel == "EXCELENTE":
                col_a, col_b = st.columns(2)
                
                with col_a:
                    ingreso_req = total_fijos_vars / target_pct if target_pct > 0 else 0
                    st.markdown(f"**Opción A: Elevar Ingresos**")
                    st.write(f"Para que tus gastos actuales sean el {target_pct*100:.0f}%, debes ganar **\$ {ingreso_req:,.2f}**:")
                    
                    ahorro_sim = ingreso_req * 0.10
                    fondo_sim = ingreso_req * 0.10
                    pct_fijos_real = (gastos_fijos / ingreso_req) * 100 if ingreso_req > 0 else 0
                    pct_vars_real = (gastos_variables / ingreso_req) * 100 if ingreso_req > 0 else 0
                    excedente = ingreso_req - (gastos_fijos + gastos_variables + ahorro_sim + fondo_sim)
                    
                    cats = [f"Fijos ({pct_fijos_real:.1f}%)", f"Variables ({pct_vars_real:.1f}%)", "Ahorro (10%)", "Inversión (10%)"]
                    montos = [gastos_fijos, gastos_variables, ahorro_sim, fondo_sim]
                    
                    if excedente > 0.01:
                        cats.append(f"Excedente ({(excedente/ingreso_req)*100:.1f}%)")
                        montos.append(excedente)
                        
                    df_a = pd.DataFrame({"Categoría": cats, "Presupuesto": montos})
                    df_a["Presupuesto"] = df_a["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                    st.table(df_a)

                with col_b:
                    ingreso_ideal = gastos_fijos / 0.50 if gastos_fijos > 0 else 0
                    st.markdown(f"**Opción B: Estructura Ideal**")
                    st.write(f"Para que tus Fijos actuales sean exactamente el 50%, debes ganar **\$ {ingreso_ideal:,.2f}**:")
                    
                    var_sim = ingreso_ideal * 0.20
                    ahorro_sim = ingreso_ideal * 0.10
                    fondo_sim = ingreso_ideal * 0.10
                    excedente_sim = ingreso_ideal * 0.10
                    
                    df_b = pd.DataFrame({
                        "Categoría": ["Fijos (50%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)", "Excedente Libre (10%)"],
                        "Presupuesto": [gastos_fijos, var_sim, ahorro_sim, fondo_sim, excedente_sim]
                    })
                    df_b["Presupuesto"] = df_b["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                    st.table(df_b)
                
            # REGLA PARA ACEPTABLE
            else:
                # SI ESTÁ CRÍTICO: Solo proponemos aumentar ingresos o estructura ideal
                if es_critico:
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        ingreso_req = total_fijos_vars / target_pct if target_pct > 0 else 0
                        st.markdown(f"**Opción A: Elevar Ingresos**")
                        st.write(f"Para que tus gastos actuales sean el {target_pct*100:.0f}%, debes ganar **\$ {ingreso_req:,.2f}**:")
                        
                        ahorro_b = ingreso_req * 0.10
                        fondo_b = ingreso_req * 0.10
                        pct_fijos_b = (gastos_fijos / ingreso_req) * 100 if ingreso_req > 0 else 0
                        pct_vars_b = (gastos_variables / ingreso_req) * 100 if ingreso_req > 0 else 0
                        excedente_b = ingreso_req - (gastos_fijos + gastos_variables + ahorro_b + fondo_b)
                        
                        cats_b = [f"Fijos ({pct_fijos_b:.1f}%)", f"Variables ({pct_vars_b:.1f}%)", "Ahorro (10%)", "Inversión (10%)"]
                        montos_b = [gastos_fijos, gastos_variables, ahorro_b, fondo_b]
                        
                        if excedente_b > 0.01:
                            cats_b.append(f"Excedente ({(excedente_b/ingreso_req)*100:.1f}%)")
                            montos_b.append(excedente_b)
                        
                        df_a_crit = pd.DataFrame({"Categoría": cats_b, "Presupuesto": montos_b})
                        df_a_crit["Presupuesto"] = df_a_crit["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                        st.table(df_a_crit)

                    with col_b:
                        ingreso_ideal = gastos_fijos / 0.60 if gastos_fijos > 0 else 0
                        st.markdown(f"**Opción B: Estructura Ideal**")
                        st.write(f"Para que tus Fijos actuales sean exactamente el 60%, debes ganar **\$ {ingreso_ideal:,.2f}**:")
                        
                        var_sim = ingreso_ideal * 0.20
                        ahorro_sim = ingreso_ideal * 0.10
                        fondo_sim = ingreso_ideal * 0.10
                        
                        df_b_crit = pd.DataFrame({
                            "Categoría": ["Fijos (60%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)"],
                            "Presupuesto": [gastos_fijos, var_sim, ahorro_sim, fondo_sim]
                        })
                        df_b_crit["Presupuesto"] = df_b_crit["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                        st.table(df_b_crit)
                        
                # SI ESTÁ ACEPTABLE: Mantenemos las tres opciones
                else:
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.markdown(f"**Opción A: Ajustar Gastos**")
                        st.write(f"Manteniendo tu ingreso de **\$ {ingresos:,.2f}** y tus Fijos bloqueados:")
                        
                        fijos_a = gastos_fijos
                        ahorro_a = ingresos * 0.10
                        fondo_a = ingresos * 0.10
                        var_a = ingresos - fijos_a - ahorro_a - fondo_a
                        
                        if var_a < 0:
                            st.error("⚠️ Gastos fijos muy altos. Matemáticamente imposible sin elevar ingresos.")
                        
                        pct_fijos_a = (fijos_a / ingresos) * 100 if ingresos > 0 else 0
                        pct_var_a = (var_a / ingresos) * 100 if ingresos > 0 else 0
                        
                        df_a = pd.DataFrame({
                            "Categoría": [f"Fijos ({pct_fijos_a:.1f}%)", f"Variables Ajustados ({pct_var_a:.1f}%)", "Ahorro (10%)", "Inversión (10%)"],
                            "Presupuesto": [fijos_a, var_a, ahorro_a, fondo_a]
                        })
                        df_a["Presupuesto"] = df_a["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                        st.table(df_a)

                    with col_b:
                        ingreso_req = total_fijos_vars / target_pct if target_pct > 0 else 0
                        st.markdown(f"**Opción B: Elevar Ingresos**")
                        st.write(f"Para que tus gastos actuales sean el {target_pct*100:.0f}%, debes ganar **\$ {ingreso_req:,.2f}**:")
                        
                        ahorro_b = ingreso_req * 0.10
                        fondo_b = ingreso_req * 0.10
                        pct_fijos_b = (gastos_fijos / ingreso_req) * 100 if ingreso_req > 0 else 0
                        pct_vars_b = (gastos_variables / ingreso_req) * 100 if ingreso_req > 0 else 0
                        excedente_b = ingreso_req - (gastos_fijos + gastos_variables + ahorro_b + fondo_b)
                        
                        cats_b = [f"Fijos ({pct_fijos_b:.1f}%)", f"Variables ({pct_vars_b:.1f}%)", "Ahorro (10%)", "Inversión (10%)"]
                        montos_b = [gastos_fijos, gastos_variables, ahorro_b, fondo_b]
                        
                        if excedente_b > 0.01:
                            cats_b.append(f"Excedente ({(excedente_b/ingreso_req)*100:.1f}%)")
                            montos_b.append(excedente_b)
                        
                        df_b = pd.DataFrame({"Categoría": cats_b, "Presupuesto": montos_b})
                        df_b["Presupuesto"] = df_b["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                        st.table(df_b)

                    with col_c:
                        ingreso_ideal = gastos_fijos / 0.60 if gastos_fijos > 0 else 0
                        st.markdown(f"**Opción C: Estructura Ideal**")
                        st.write(f"Para que tus Fijos actuales sean exactamente el 60%, debes ganar **\$ {ingreso_ideal:,.2f}**:")
                        
                        var_sim = ingreso_ideal * 0.20
                        ahorro_sim = ingreso_ideal * 0.10
                        fondo_sim = ingreso_ideal * 0.10
                        
                        df_c = pd.DataFrame({
                            "Categoría": ["Fijos (60%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)"],
                            "Presupuesto": [gastos_fijos, var_sim, ahorro_sim, fondo_sim]
                        })
                        df_c["Presupuesto"] = df_c["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                        st.table(df_c)

        # Disparador de recomendaciones
        if estado == "CRÍTICO":
            if not (balance < 0): 
                st.warning("⚠️ **Estrategia sugerida:** Dado tu estatus, la prioridad es inyectar capital para ajustar tus porcentajes. Aquí tienes los números objetivo:")
            
            mostrar_planes("ACEPTABLE", 0.80, es_critico=True)
            st.divider()
            mostrar_planes("EXCELENTE", 0.70, es_critico=True)
            
        elif estado == "ACEPTABLE":
            mostrar_planes("EXCELENTE", 0.70)
