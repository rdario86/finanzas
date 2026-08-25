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

        # Función de planes de acción con parámetro de criticidad
        def mostrar_planes(nivel, target_pct, es_critico=False):
            st.subheader(f"💡 Plan de Acción para lograr estado: {nivel}")
            
            # REGLA PARA EXCELENTE: Dos opciones (siempre orientadas a aumento de ingresos)
            if nivel == "EXCELENTE":
                col_a, col_b = st.columns(2)
                
                # --- OPCIÓN A: AUMENTAR INGRESOS ---
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

                # --- OPCIÓN B: HÍBRIDA SOBRE INGRESO DE OPCIÓN A ---
                with col_b:
                    st.markdown(f"**Opción B: Estructura Híbrida**")
                    st.write(f"Con el ingreso de la Opción A (**\$ {ingreso_req:,.2f}**), manteniendo tus Fijos intactos y aplicando 20/10/10:")
                    
                    fijos_sim_b = gastos_fijos
                    var_sim_b = ingreso_req * 0.20
                    ahorro_sim_b = ingreso_req * 0.10
                    fondo_sim_b = ingreso_req * 0.10
                    
                    pct_fijos_b = (fijos_sim_b / ingreso_req) * 100 if ingreso_req > 0 else 0
                    excedente_b = ingreso_req - (fijos_sim_b + var_sim_b + ahorro_sim_b + fondo_sim_b)
                    
                    cats_b = [f"Fijos ({pct_fijos_b:.1f}%)", "Variables (20.0%)", "Ahorro (10.0%)", "Inversión (10.0%)"]
                    montos_b = [fijos_sim_b, var_sim_b, ahorro_sim_b, fondo_sim_b]
                    
                    if excedente_b > 0.01:
                        cats_b.append(f"Excedente Libre ({(excedente_b/ingreso_req)*100:.1f}%)")
                        montos_b.append(excedente_b)
                    elif excedente_b < -0.01:
                        cats_b.append(f"Déficit Matemático ({(abs(excedente_b)/ingreso_req)*100:.1f}%)")
                        montos_b.append(excedente_b)
                        
                    df_b = pd.DataFrame({"Categoría": cats_b, "Presupuesto": montos_b})
                    df_b["Presupuesto"] = df_b["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                    st.table(df_b)
                
            # REGLA PARA ACEPTABLE
            else:
                # SI ESTÁ CRÍTICO, OMITIMOS LA OPCIÓN DE RECORTAR GASTOS CON INGRESO ACTUAL
                if es_critico:
                    col_a, col_b = st.columns(2)
                    
                    # --- OPCIÓN A (ANTES B): AUMENTAR INGRESOS ---
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
                        
                        df_b = pd.DataFrame({"Categoría": cats_b, "Presupuesto": montos_b})
                        df_b["Presupuesto"] = df_b["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                        st.table(df_b)

                    # --- OPCIÓN B (ANTES C): HÍBRIDA SOBRE NUEVO INGRESO ---
                    with col_b:
                        st.markdown(f"**Opción B: Estructura Híbrida**")
                        st.write(f"Con el ingreso de Opción A (**\$ {ingreso_req:,.2f}**), manteniendo tus Fijos intactos y aplicando 20/10/10:")
                        
                        fijos_c = gastos_fijos
                        var_c = ingreso_req * 0.20
                        ahorro_c = ingreso_req * 0.10
                        fondo_c = ingreso_req * 0.10
                        
                        pct_fijos_c = (fijos_c / ingreso_req) * 100 if ingreso_req > 0 else 0
                        excedente_c = ingreso_req - (fijos_c + var_c + ahorro_c + fondo_c)
                        
                        cats_c = [f"Fijos ({pct_fijos_c:.1f}%)", "Variables (20.0%)", "Ahorro (10.0%)", "Inversión (10.0%)"]
                        montos_c = [fijos_c, var_c, ahorro_c, fondo_c]
                        
                        if excedente_c > 0.01:
                            cats_c.append(f"Excedente Libre ({(excedente_c/ingreso_req)*100:.1f}%)")
                            montos_c.append(excedente_c)
                        elif excedente_c < -0.01:
                            cats_c.append(f"Déficit Matemático ({(abs(excedente_c)/ingreso_req)*100:.1f}%)")
                            montos_c.append(excedente_c)
                            
                        df_c = pd.DataFrame({"Categoría": cats_c, "Presupuesto": montos_c})
                        df_c["Presupuesto"] = df_c["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                        st.table(df_c)
                        
                # SI ESTÁ ACEPTABLE, MANTENEMOS LAS TRES OPCIONES ORIGINALES
                else:
                    col_a, col_b, col_c = st.columns(3)
                    
                    # --- OPCIÓN A: REESTRUCTURAR GASTOS ---
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

                    # --- OPCIÓN B: AUMENTAR INGRESOS ---
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

                    # --- OPCIÓN C: HÍBRIDA SOBRE INGRESO DE OPCIÓN B ---
                    with col_c:
                        st.markdown(f"**Opción C: Estructura Híbrida**")
                        st.write(f"Con el ingreso de Opción B (**\$ {ingreso_req:,.2f}**), manteniendo tus Fijos intactos y aplicando 20/10/10:")
                        
                        fijos_c = gastos_fijos
                        var_c = ingreso_req * 0.20
                        ahorro_c = ingreso_req * 0.10
                        fondo_c = ingreso_req * 0.10
                        
                        pct_fijos_c = (fijos_c / ingreso_req) * 100 if ingreso_req > 0 else 0
                        excedente_c = ingreso_req - (fijos_c + var_c + ahorro_c + fondo_c)
                        
                        cats_c = [f"Fijos ({pct_fijos_c:.1f}%)", "Variables (20.0%)", "Ahorro (10.0%)", "Inversión (10.0%)"]
                        montos_c = [fijos_c, var_c, ahorro_c, fondo_c]
                        
                        if excedente_c > 0.01:
                            cats_c.append(f"Excedente Libre ({(excedente_c/ingreso_req)*100:.1f}%)")
                            montos_c.append(excedente_c)
                        elif excedente_c < -0.01:
                            cats_c.append(f"Déficit Matemático ({(abs(excedente_c)/ingreso_req)*100:.1f}%)")
                            montos_c.append(excedente_c)
                            
                        df_c = pd.DataFrame({"Categoría": cats_c, "Presupuesto": montos_c})
                        df_c["Presupuesto"] = df_c["Presupuesto"].apply(lambda x: f"$ {x:,.2f}")
                        st.table(df_c)

        # Disparador de recomendaciones
        if estado == "CRÍTICO":
            st.warning("⚠️ **Estrategia sugerida:** Dado tu estado actual, la prioridad técnica no es recortar, sino inyectar capital. Aquí tienes los números objetivo:")
            mostrar_planes("ACEPTABLE", 0.80, es_critico=True)
            st.divider()
            mostrar_planes("EXCELENTE", 0.70, es_critico=True)
            
        elif estado == "ACEPTABLE":
            mostrar_planes("EXCELENTE", 0.70)
