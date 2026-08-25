import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Diagnóstico Financiero", page_icon="📊", layout="wide")

# Encabezado principal
st.title("Diagnóstico Financiero 📊")
st.markdown("#### Panel de Control")

# Leyenda con las reglas exactas
with st.expander("ℹ️ Regla de Evaluación: El peso de tus Gastos Fijos"):
    st.markdown("""
    La salud de tu estructura se mide por el porcentaje que consumen tus **Gastos Fijos** sobre tus **Ingresos Totales**:
    
    - 🟢 **EXCELENTE:** < 50%
    - 🟡 **ACEPTABLE:** >= 50% y <= 60%
    - 🔴 **CRÍTICO:** > 60% (Y *CRÍTICO EXTREMO* si tus fijos superan el 100% de lo que ganas).
    """)

st.divider()

st.header("1. Ingresa tus datos mensuales")

# Campos de entrada manual (Formateados a 2 decimales para mejor UX)
col1, col2 = st.columns(2)
with col1:
    ingresos = st.number_input("Ingresos Totales (\$)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
with col2:
    gastos_fijos = st.number_input("Gastos Fijos Totales (\$)", min_value=0.0, value=650.0, step=50.0, format="%.2f")

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
        
        # ==========================================================
        # 1. MEJORA: MANEJO DE DÉFICIT EXTREMO Y REGLAS ESTRICTAS
        # ==========================================================
        if pct_fijos >= 100:
            estado = "CRÍTICO EXTREMO"
            color = "#8b0000" # Rojo oscuro (DarkRed)
            mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tus ingresos. ¡Tus compromisos fijos superan o igualan tu sueldo!"
            recomendacion = "🚨 **Emergencia:** Estás en bancarrota técnica, asumiendo deudas solo para existir. Debes hacer recortes drásticos a tu estilo de vida base inmediatamente."
            
        elif pct_fijos > 60:
            estado = "CRÍTICO"
            color = "#dc3545" # Rojo
            mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tus ingresos. Estás por encima del límite de riesgo (> 60%)."
            recomendacion = "⚠️ **Recomendación:** Tu estilo de vida base es demasiado costoso para tu nivel de ingresos actual. Revisa las metas de ingresos requeridos más abajo."
            
        elif pct_fijos >= 50 and pct_fijos <= 60:
            estado = "ACEPTABLE"
            color = "#ffc107" # Amarillo
            mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tus ingresos. Te mantienes en la zona de equilibrio (>= 50% y <= 60%)."
            recomendacion = "✅ **Recomendación:** Tienes una estructura sana. Vigila que tus gastos fijos no suban y revisa abajo tu meta para pasar al siguiente nivel (EXCELENTE)."
            
        elif pct_fijos < 50:
            estado = "EXCELENTE"
            color = "#28a745" # Verde
            mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tus ingresos. Tienes una flexibilidad financiera sobresaliente (< 50%)."
            recomendacion = "🌟 **Recomendación:** Tu estructura es robusta. Mantén tus gastos fijos controlados para maximizar tu capacidad de construir patrimonio. ¡Sigue así!"

        st.markdown(f"Estatus de tu estructura: <strong style='color:{color}; font-size: 1.5em;'>{estado}</strong>", unsafe_allow_html=True)
        st.markdown(mensaje)
        st.markdown(recomendacion)
        
        # Variable para almacenar el ingreso excelente para el reporte
        ingreso_req_excelente = gastos_fijos / 0.50
        
        # ==========================================================
        # CÁLCULO: METAS DE INGRESO CONDICIONALES Y GRÁFICOS
        # ==========================================================
        if estado != "EXCELENTE":
            st.divider()
            st.header("3. Plan de Acción: Metas de Ingreso")
            
            if estado == "CRÍTICO" or estado == "CRÍTICO EXTREMO":
                st.markdown("Tomando tus Gastos Fijos actuales de **\$ {:,.2f}** como un ancla inamovible, estos son los ingresos mínimos requeridos para sanear tu estructura:".format(gastos_fijos))
                col_a, col_b = st.columns(2)
                
                with col_a:
                    ingreso_req_aceptable = gastos_fijos / 0.60
                    st.markdown(f"### 🟡 Meta ACEPTABLE")
                    st.write("Para que tus fijos representen el **60%**, tu ingreso mínimo requerido debe ser:")
                    st.markdown(f"<h3 style='color:#ffc107;'>$ {ingreso_req_aceptable:,.2f}</h3>", unsafe_allow_html=True)
                    
                    dif_ace = ingresos - ingreso_req_aceptable
                    if dif_ace > 0:
                        st.success(f"✅ Tus ingresos actuales superan esta meta por **\$ {dif_ace:,.2f}**.")
                    elif dif_ace < 0:
                        st.warning(f"⚠️ Te faltan **\$ {abs(dif_ace):,.2f}** mensuales para alcanzar esta meta.")
                    
                    var_ace = ingreso_req_aceptable * 0.20
                    aho_ace = ingreso_req_aceptable * 0.10
                    inv_ace = ingreso_req_aceptable * 0.10
                    
                    # 2. MEJORA: Gráfico de Dona para Meta Aceptable
                    df_ace = pd.DataFrame({
                        "Distribución Ideal": ["Gastos Fijos (60%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)"],
                        "Monto Numérico": [gastos_fijos, var_ace, aho_ace, inv_ace]
                    })
                    
                    fig_ace = px.pie(df_ace, values='Monto Numérico', names='Distribución Ideal', hole=0.4, 
                                     color_discrete_sequence=['#dc3545', '#17a2b8', '#ffc107', '#28a745'])
                    fig_ace.update_layout(title_text="Estructura Aceptable", title_x=0.3, margin=dict(t=40, b=0, l=0, r=0))
                    st.plotly_chart(fig_ace, use_container_width=True)
                    
                    # Formateo de tabla
                    df_ace["Monto Meta"] = df_ace["Monto Numérico"].apply(lambda x: f"$ {x:,.2f}")
                    st.table(df_ace[["Distribución Ideal", "Monto Meta"]])

                with col_b:
                    st.markdown(f"### 🟢 Meta EXCELENTE")
                    st.write("Para que tus fijos representen el **50%**, tu ingreso mínimo requerido debe ser:")
                    st.markdown(f"<h3 style='color:#28a745;'>$ {ingreso_req_excelente:,.2f}</h3>", unsafe_allow_html=True)
                    
                    dif_exc = ingresos - ingreso_req_excelente
                    if dif_exc > 0:
                        st.success(f"✅ Tus ingresos actuales superan esta meta por **\$ {dif_exc:,.2f}**.")
                    elif dif_exc < 0:
                        st.warning(f"⚠️ Te faltan **\$ {abs(dif_exc):,.2f}** mensuales para alcanzar esta meta.")
                    
                    var_exc = ingreso_req_excelente * 0.20
                    aho_exc = ingreso_req_excelente * 0.10
                    inv_exc = ingreso_req_excelente * 0.10
                    excedente_exc = ingreso_req_excelente * 0.10
                    
                    # 2. MEJORA: Gráfico de Dona para Meta Excelente
                    df_exc = pd.DataFrame({
                        "Distribución Ideal": ["Gastos Fijos (50%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)", "Excedente Libre (10%)"],
                        "Monto Numérico": [gastos_fijos, var_exc, aho_exc, inv_exc, excedente_exc]
                    })
                    
                    fig_exc = px.pie(df_exc, values='Monto Numérico', names='Distribución Ideal', hole=0.4, 
                                     color_discrete_sequence=['#dc3545', '#17a2b8', '#ffc107', '#28a745', '#6c757d'])
                    fig_exc.update_layout(title_text="Estructura Excelente", title_x=0.3, margin=dict(t=40, b=0, l=0, r=0))
                    st.plotly_chart(fig_exc, use_container_width=True)
                    
                    # Formateo de tabla
                    df_exc["Monto Meta"] = df_exc["Monto Numérico"].apply(lambda x: f"$ {x:,.2f}")
                    st.table(df_exc[["Distribución Ideal", "Monto Meta"]])

            elif estado == "ACEPTABLE":
                st.markdown("Tomando tus Gastos Fijos actuales de **\$ {:,.2f}** como un ancla inamovible, este es el ingreso mínimo requerido para llevar tu estructura al nivel óptimo:".format(gastos_fijos))
                
                col1_acep, col2_acep = st.columns([1, 1.5])
                
                with col1_acep:
                    st.markdown(f"### 🟢 Meta para pasar a EXCELENTE")
                    st.write("Para dar el siguiente paso y que tus fijos representen el **50%**, tu ingreso mínimo requerido debe ser:")
                    st.markdown(f"<h3 style='color:#28a745;'>$ {ingreso_req_excelente:,.2f}</h3>", unsafe_allow_html=True)
                    
                    dif_exc = ingresos - ingreso_req_excelente
                    if dif_exc < 0:
                        st.warning(f"⚠️ Te faltan **\$ {abs(dif_exc):,.2f}** mensuales para alcanzar esta meta.")
                    else:
                        st.info("🎯 Tus ingresos actuales están exactamente en esta meta.")
                    
                    var_exc = ingreso_req_excelente * 0.20
                    aho_exc = ingreso_req_excelente * 0.10
                    inv_exc = ingreso_req_excelente * 0.10
                    excedente_exc = ingreso_req_excelente * 0.10
                    
                    df_exc = pd.DataFrame({
                        "Distribución Ideal": ["Gastos Fijos (50%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)", "Excedente Libre (10%)"],
                        "Monto Numérico": [gastos_fijos, var_exc, aho_exc, inv_exc, excedente_exc]
                    })
                    
                    df_exc["Monto Meta"] = df_exc["Monto Numérico"].apply(lambda x: f"$ {x:,.2f}")
                    st.table(df_exc[["Distribución Ideal", "Monto Meta"]])
                
                with col2_acep:
                    # 2. MEJORA: Gráfico de Dona 
                    fig_exc = px.pie(df_exc, values='Monto Numérico', names='Distribución Ideal', hole=0.4, 
                                     color_discrete_sequence=['#dc3545', '#17a2b8', '#ffc107', '#28a745', '#6c757d'])
                    fig_exc.update_layout(title_text="Distribución Excelente (50%)", title_x=0.5)
                    st.plotly_chart(fig_exc, use_container_width=True)

        st.divider()
        
        # ==========================================================
        # 4. MEJORA: BOTÓN PARA DESCARGAR EL DIAGNÓSTICO
        # ==========================================================
        st.subheader("📥 Llévate tu diagnóstico")
        st.write("Descarga un resumen de texto con tus resultados para tener siempre a mano tu meta de ingresos.")
        
        # Creando el texto del reporte
        reporte = f"""=========================================
DIAGNÓSTICO FINANCIERO - RESULTADOS
=========================================
Ingresos Actuales Estimados: ${ingresos:,.2f}
Gastos Fijos Actuales:       ${gastos_fijos:,.2f}
Peso de tus Gastos Fijos:    {pct_fijos:.1f}%

ESTATUS ACTUAL: {estado}
Recomendación: {recomendacion}
=========================================
"""
        if estado != "EXCELENTE":
            reporte += f"\nPLAN DE ACCIÓN - META EXCELENTE (50%):\n"
            reporte += f"Para sanear tu estructura, tu Ingreso Mínimo Requerido debe ser: ${ingreso_req_excelente:,.2f}\n"
            reporte += f"Diferencia con tu ingreso actual: ${abs(ingresos - ingreso_req_excelente):,.2f}\n"
