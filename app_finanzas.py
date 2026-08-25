import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diagnóstico Financiero", page_icon="📊", layout="centered")

# Encabezado principal
st.title("Diagnóstico Financiero 📊")
st.markdown("#### Panel de Control - Rubén Núñez")
st.markdown("Ingresa tus ingresos y tus gastos fijos para evaluar tu estructura y calcular tu meta de ingresos ideal.")

# Leyenda con las reglas
with st.expander("ℹ️ Regla de Evaluación: El peso de tus Gastos Fijos"):
    st.markdown("""
    La salud de tu estructura se mide por el porcentaje que consumen tus **Gastos Fijos** sobre tus **Ingresos Totales**:
    
    - 🟢 **EXCELENTE:** Menos del 50%.
    - 🟡 **ACEPTABLE:** Entre el 50% y el 60%.
    - 🔴 **CRÍTICO:** Más del 60%.
    """)

st.divider()

st.header("1. Ingresa tus datos mensuales")

# Solo dos campos de entrada
col1, col2 = st.columns(2)
with col1:
    ingresos = st.number_input("Ingresos Totales (\$)", min_value=0.0, value=1000.0, step=100.0)
with col2:
    gastos_fijos = st.number_input("Gastos Fijos Totales (\$)", min_value=0.0, value=650.0, step=50.0)

if st.button("Generar Diagnóstico", type="primary"):
    
    if ingresos == 0:
        st.error("Los ingresos deben ser mayores a $0 para realizar el cálculo.")
    elif gastos_fijos == 0:
        st.error("Por favor, ingresa un monto válido para tus Gastos Fijos.")
    else:
        st.divider()
        st.header("2. Tu Diagnóstico Actual")
        
        # El diagnóstico evalúa el peso de los fijos sobre los ingresos reales
        pct_fijos = (gastos_fijos / ingresos) * 100
        
        if pct_fijos > 60:
            estado = "CRÍTICO"
            color = "#dc3545" # Rojo
            mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tus ingresos. Estás por encima del límite de riesgo."
            recomendacion = "⚠️ **Recomendación:** Tu estilo de vida base es demasiado costoso para tu nivel de ingresos actual. Revisa las metas de ingresos requeridos más abajo."
        elif pct_fijos >= 50:
            estado = "ACEPTABLE"
            color = "#ffc107" # Amarillo
            mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tus ingresos. Te mantienes en la zona de equilibrio."
            recomendacion = "✅ **Recomendación:** Tienes una estructura sana. Vigila que tus gastos fijos no suban y revisa abajo tu meta para pasar al siguiente nivel."
        else:
            estado = "EXCELENTE"
            color = "#28a745" # Verde
            mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tus ingresos. Tienes una flexibilidad financiera sobresaliente."
            recomendacion = "🌟 **Recomendación:** Tu estructura es robusta. Mantén tus gastos fijos controlados para maximizar tu capacidad de construir patrimonio. ¡Sigue así, no necesitas un plan de rescate!"

        st.markdown(f"Estatus de tu estructura: <strong style='color:{color}; font-size: 1.5em;'>{estado}</strong>", unsafe_allow_html=True)
        st.markdown(mensaje)
        st.markdown(recomendacion)
        
        # ==========================================================
        # CÁLCULO: METAS DE INGRESO CONDICIONALES
        # ==========================================================
        if estado != "EXCELENTE":
            st.divider()
            st.header("3. Plan de Acción: Metas de Ingreso")
            st.markdown("Tomando tus Gastos Fijos actuales de **\$ {:,.2f}** como un ancla inamovible, estos son los ingresos mínimos requeridos para sanear tu estructura:".format(gastos_fijos))
            
            # SI ESTÁ CRÍTICO: MOSTRAR ACEPTABLE Y EXCELENTE
            if estado == "CRÍTICO":
                col_a, col_b = st.columns(2)
                
                with col_a:
                    # Meta Aceptable (Fijos al 60%)
                    ingreso_req_aceptable = gastos_fijos / 0.60
                    
                    st.markdown(f"### 🟡 Meta ACEPTABLE")
                    st.write("Para que tus fijos representen el **60%**, tu ingreso mínimo requerido debe ser:")
                    st.markdown(f"<h3 style='color:#ffc107;'>$ {ingreso_req_aceptable:,.2f}</h3>", unsafe_allow_html=True)
                    
                    dif_ace = ingresos - ingreso_req_aceptable
                    if dif_ace > 0:
                        st.success(f"✅ Tus ingresos actuales superan esta meta por **\$ {dif_ace:,.2f}**.")
                    elif dif_ace < 0:
                        st.warning(f"⚠️ Te faltan **\$ {abs(dif_ace):,.2f}** mensuales para alcanzar esta meta.")
                    else:
                        st.info("🎯 Tus ingresos actuales están exactamente en esta meta.")
                    
                    var_ace = ingreso_req_aceptable * 0.20
                    aho_ace = ingreso_req_aceptable * 0.10
                    inv_ace = ingreso_req_aceptable * 0.10
                    
                    df_ace = pd.DataFrame({
                        "Distribución Ideal": ["Gastos Fijos (60%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)"],
                        "Monto Meta": [gastos_fijos, var_ace, aho_ace, inv_ace]
                    })
                    df_ace["Monto Meta"] = df_ace["Monto Meta"].apply(lambda x: f"$ {x:,.2f}")
                    st.table(df_ace)

                with col_b:
                    # Meta Excelente (Fijos al 50%)
                    ingreso_req_excelente = gastos_fijos / 0.50
                    
                    st.markdown(f"### 🟢 Meta EXCELENTE")
                    st.write("Para que tus fijos representen el **50%**, tu ingreso mínimo requerido debe ser:")
                    st.markdown(f"<h3 style='color:#28a745;'>$ {ingreso_req_excelente:,.2f}</h3>", unsafe_allow_html=True)
                    
                    dif_exc = ingresos - ingreso_req_excelente
                    if dif_exc > 0:
                        st.success(f"✅ Tus ingresos actuales superan esta meta por **\$ {dif_exc:,.2f}**.")
                    elif dif_exc < 0:
                        st.warning(f"⚠️ Te faltan **\$ {abs(dif_exc):,.2f}** mensuales para alcanzar esta meta.")
                    else:
                        st.info("🎯 Tus ingresos actuales están exactamente en esta meta.")
                    
                    var_exc = ingreso_req_excelente * 0.20
                    aho_exc = ingreso_req_excelente * 0.10
                    inv_exc = ingreso_req_excelente * 0.10
                    excedente_exc = ingreso_req_excelente * 0.10
                    
                    df_exc = pd.DataFrame({
                        "Distribución Ideal": ["Gastos Fijos (50%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)", "Excedente Libre (10%)"],
                        "Monto Meta": [gastos_fijos, var_exc, aho_exc, inv_exc, excedente_exc]
                    })
                    df_exc["Monto Meta"] = df_exc["Monto Meta"].apply(lambda x: f"$ {x:,.2f}")
                    st.table(df_exc)
            
            # SI ESTÁ ACEPTABLE: MOSTRAR SOLO EXCELENTE
            elif estado == "ACEPTABLE":
                ingreso_req_excelente = gastos_fijos / 0.50
                
                st.markdown(f"### 🟢 Meta para pasar a EXCELENTE")
                st.write("Para dar el siguiente paso y que tus fijos representen el **50%**, tu ingreso mínimo requerido debe ser:")
                st.markdown(f"<h3 style='color:#28a745;'>$ {ingreso_req_excelente:,.2f}</h3>", unsafe_allow_html=True)
                
                dif_exc = ingresos - ingreso_req_excelente
                if dif_exc > 0:
                    st.success(f"✅ Tus ingresos actuales superan esta meta por **\$ {dif_exc:,.2f}**.")
                elif dif_exc < 0:
                    st.warning(f"⚠️ Te faltan **\$ {abs(dif_exc):,.2f}** mensuales para alcanzar esta meta.")
                else:
                    st.info("🎯 Tus ingresos actuales están exactamente en esta meta.")
                
                var_exc = ingreso_req_excelente * 0.20
                aho_exc = ingreso_req_excelente * 0.10
                inv_exc = ingreso_req_excelente * 0.10
                excedente_exc = ingreso_req_excelente * 0.10
                
                df_exc = pd.DataFrame({
                    "Distribución Ideal": ["Gastos Fijos (50%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)", "Excedente Libre (10%)"],
                    "Monto Meta": [gastos_fijos, var_exc, aho_exc, inv_exc, excedente_exc]
                })
                df_exc["Monto Meta"] = df_exc["Monto Meta"].apply(lambda x: f"$ {x:,.2f}")
                
                # Se renderiza en una sola columna centrada visualmente
                col1_acep, col2_acep = st.columns([1.5, 1])
                with col1_acep:
                    st.table(df_exc)
