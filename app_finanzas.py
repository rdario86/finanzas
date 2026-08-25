import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diagnóstico Financiero", page_icon="📊", layout="centered")

# Encabezado principal
st.title("Diagnóstico Financiero 📊")
st.markdown("#### Panel de Control - Rubén Núñez")
st.markdown("Ingresa tus salidas de dinero mensuales para evaluar la estructura de tus finanzas y descubrir tu meta de ingresos.")

# Leyenda con las nuevas reglas
with st.expander("ℹ️ Regla de Evaluación: El peso de tus Gastos Fijos"):
    st.markdown("""
    La salud de tu estructura financiera se mide evaluando qué porcentaje de tu dinero es consumido por tus **Gastos Fijos** (aquellos que debes pagar sí o sí cada mes):
    
    - 🟢 **EXCELENTE:** Tus gastos fijos consumen **menos del 50%** de tu flujo.
    - 🟡 **ACEPTABLE:** Tus gastos fijos consumen **entre el 50% y el 60%**.
    - 🔴 **CRÍTICO:** Tus gastos fijos consumen **más del 60%** (Vives al límite y sin margen de maniobra).
    """)

st.divider()

st.header("1. Ingresa tus salidas mensuales")

# Campos de entrada directa (sin barra deslizadora)
col1, col2 = st.columns(2)
with col1:
    gastos_fijos = st.number_input("Gastos Fijos Totales (\$)", min_value=0.0, value=650.0, step=50.0)
    gastos_variables = st.number_input("Gastos Variables Totales (\$)", min_value=0.0, value=200.0, step=50.0)
with col2:
    ahorro = st.number_input("Destinado a Ahorro (\$)", min_value=0.0, value=50.0, step=10.0)
    fondo_inversion = st.number_input("Destinado a Fondo/Inversión (\$)", min_value=0.0, value=50.0, step=10.0)

if st.button("Generar Diagnóstico", type="primary"):
    
    # El flujo de caja estimado es la suma de todo el dinero que el usuario distribuye
    flujo_total = gastos_fijos + gastos_variables + ahorro + fondo_inversion
    
    if flujo_total == 0:
        st.error("Debes ingresar montos mayores a \$0 para realizar el cálculo.")
    elif gastos_fijos == 0:
        st.error("Los Gastos Fijos son la base del diagnóstico. Por favor, ingresa un monto válido.")
    else:
        st.divider()
        st.header("2. Tu Diagnóstico Actual")
        
        st.info(f"💡 Sumando todas tus categorías, estimamos que tu flujo de dinero actual es de **\$ {flujo_total:,.2f}** al mes.")
        
        # El diagnóstico se basa ÚNICAMENTE en el peso de los fijos
        pct_fijos = (gastos_fijos / flujo_total) * 100
        
        if pct_fijos > 60:
            estado = "CRÍTICO"
            color = "#dc3545" # Rojo
            mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tu dinero. Estás por encima del límite de riesgo."
            recomendacion = "⚠️ **Recomendación:** Tu estilo de vida base es demasiado costoso para tu flujo actual. Debes enfocarte urgentemente en reducir contratos fijos o trazar un plan para aumentar tus ingresos."
        elif pct_fijos >= 50:
            estado = "ACEPTABLE"
            color = "#ffc107" # Amarillo
            mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tu dinero. Te mantienes en la zona de equilibrio."
            recomendacion = "✅ **Recomendación:** Tienes una estructura sana. Vigila que tus gastos fijos no suban y busca optimizar tus excedentes hacia la inversión."
        else:
            estado = "EXCELENTE"
            color = "#28a745" # Verde
            mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tu dinero. Tienes una flexibilidad financiera sobresaliente."
            recomendacion = "🌟 **Recomendación:** Tu estructura es robusta. Mantén tus gastos fijos controlados para maximizar tu capacidad de construir patrimonio."

        st.markdown(f"Estatus de tu estructura: <strong style='color:{color}; font-size: 1.5em;'>{estado}</strong>", unsafe_allow_html=True)
        st.markdown(mensaje)
        st.markdown(recomendacion)
        
        st.divider()

        # ==========================================================
        # PLAN DE ACCIÓN: METAS DE INGRESO
        # ==========================================================
        st.header("3. Plan de Acción: Metas de Ingreso")
        st.markdown("Manteniendo tus Gastos Fijos actuales de **\$ {:,.2f}** como un ancla inamovible, estos son los ingresos mínimos requeridos para lograr una estructura óptima:".format(gastos_fijos))
        
        # Columnas para mostrar los dos escenarios ideales
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Meta Aceptable (Fijos al 60%)
            ingreso_req_aceptable = gastos_fijos / 0.60
            
            st.markdown(f"### 🟡 Meta ACEPTABLE")
            st.write("Para que tus fijos representen el **60%**, tu ingreso mínimo requerido debe ser:")
            st.markdown(f"<h3 style='color:#ffc107;'>$ {ingreso_req_aceptable:,.2f}</h3>", unsafe_allow_html=True)
            
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
            
            # En Excelente (50%), sobra un 10% adicional si usamos 20/10/10 para el resto
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
