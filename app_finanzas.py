import streamlit as st
import pandas as pd

st.set_page_config(page_title="Diagnóstico Financiero", page_icon="📊", layout="wide")

# Encabezado personalizado
st.title("Diagnóstico Financiero 📊")
st.markdown("#### Panel de Control - Rubén Núñez")
st.markdown("Ingresa tus salidas mensuales actuales para descubrir tu meta de ingresos ideal.")

# Nueva Leyenda del Diagnóstico (Regla de Fijos)
with st.expander("ℹ️ Nueva Regla: ¿Cómo se evalúa el estatus financiero?"):
    st.markdown("""
    El estado de tus finanzas se determina ahora **exclusivamente** por el porcentaje que representan tus **Gastos Fijos** sobre el total de tus salidas (tu ingreso actual estimado):
    - 🟢 **EXCELENTE:** Gastos fijos son menores al **50%**.
    - 🟡 **ACEPTABLE:** Gastos fijos entre el **50%** y el **60%**.
    - 🔴 **CRÍTICO:** Gastos fijos mayores al **60%**.
    
    *La meta recomendada para estructurar tu presupuesto siempre será el método **60/20/10/10** (o 50/20/10/10 para el nivel Excelente).*
    """)

st.divider()

st.header("1. Ingresa tus salidas mensuales")

# Entradas manuales (Sin campo de Ingresos Totales)
col1, col2 = st.columns(2)
with col1:
    gastos_fijos = st.number_input("Gastos Fijos (\$)", min_value=0.0, value=650.0, step=50.0)
    gastos_variables = st.number_input("Gastos Variables (\$)", min_value=0.0, value=200.0, step=50.0)
with col2:
    ahorro = st.number_input("Ahorro (\$)", min_value=0.0, value=50.0, step=10.0)
    fondo_reserva = st.number_input("Fondo/Inversión (\$)", min_value=0.0, value=50.0, step=10.0)

if st.button("Hacer Diagnóstico", type="primary"):
    
    # El ingreso actual implícito es simplemente la suma de todo lo que el usuario distribuye hoy
    ingreso_actual_implicito = gastos_fijos + gastos_variables + ahorro + fondo_reserva
    
    if ingreso_actual_implicito == 0:
        st.error("Debes ingresar montos mayores a \$0 para calcular tu diagnóstico.")
    elif gastos_fijos == 0:
        st.error("Debes registrar tus Gastos Fijos para poder proyectar tu ingreso ideal.")
    else:
        st.divider()
        st.header("2. Resultados del Diagnóstico Actual")
        
        st.info(f"💡 Sumando tus gastos y asignaciones actuales, estimamos que tu nivel de ingresos (o flujo de caja) mensual es de **\$ {ingreso_actual_implicito:,.2f}**.")
        
        # Análisis del Estatus (Basado SOLO en Gastos Fijos)
        pct_fijos = (gastos_fijos / ingreso_actual_implicito) * 100
        
        if pct_fijos > 60:
            estado = "CRÍTICO"
            color = "#dc3545" # Rojo
            mensaje = f"Tus Gastos Fijos representan el **{pct_fijos:.1f}%** de tus salidas totales. Superan el límite seguro del 60%."
        elif pct_fijos >= 50:
            estado = "ACEPTABLE"
            color = "#ffc107" # Amarillo
            mensaje = f"Tus Gastos Fijos representan el **{pct_fijos:.1f}%** de tus salidas totales. Están dentro del rango saludable (50%-60%)."
        else:
            estado = "EXCELENTE"
            color = "#28a745" # Verde
            mensaje = f"Tus Gastos Fijos representan el **{pct_fijos:.1f}%** de tus salidas totales. ¡Tienes una estructura muy ligera (por debajo del 50%)!"

        st.markdown(mensaje)
        st.markdown(f"Estatus actual de tu estructura: <strong style='color:{color}; font-size: 1.3em;'>{estado}</strong>", unsafe_allow_html=True)

        st.divider()
        
        # 3. Recomendaciones de Ingreso Ideal
        st.header("3. Proyecciones de Ingreso Ideal")
        st.markdown(f"Basándonos en que tus **Gastos Fijos (\$ {gastos_fijos:,.2f})** son inamovibles, estas son las metas de facturación que debes perseguir para optimizar tu estructura:")
        
        col_a, col_b = st.columns(2)
        
        # --- PROYECCIÓN ACEPTABLE (Fijos = 60%) ---
        with col_a:
            ingreso_aceptable = gastos_fijos / 0.60
            st.subheader("🟡 Meta ACEPTABLE")
            st.write("Para que tus Fijos representen el 60%, tu ingreso debe ser:")
            st.markdown(f"<h3 style='color:#ffc107;'>$ {ingreso_aceptable:,.2f}</h3>", unsafe_allow_html=True)
            
            var_a = ingreso_aceptable * 0.20
            ahorro_a = ingreso_aceptable * 0.10
            fondo_a = ingreso_aceptable * 0.10
            
            df_a = pd.DataFrame({
                "Categoría": ["Gastos Fijos (60%)", "Gastos Variables (20%)", "Ahorro (10%)", "Fondo/Inversión (10%)"],
                "Presupuesto Meta": [gastos_fijos, var_a, ahorro_a, fondo_a]
            })
            df_a["Presupuesto Meta"] = df_a["Presupuesto Meta"].apply(lambda x: f"$ {x:,.2f}")
            st.table(df_a)
            
        # --- PROYECCIÓN EXCELENTE (Fijos = 50%) ---
        with col_b:
            ingreso_excelente = gastos_fijos / 0.50
            st.subheader("🟢 Meta EXCELENTE")
            st.write("Para que tus Fijos representen el 50%, tu ingreso debe ser:")
            st.markdown(f"<h3 style='color:#28a745;'>$ {ingreso_excelente:,.2f}</h3>", unsafe_allow_html=True)
            
            var_e = ingreso_excelente * 0.20
            ahorro_e = ingreso_excelente * 0.10
            fondo_e = ingreso_excelente * 0.10
            excedente_e = ingreso_excelente * 0.10
            
            df_e = pd.DataFrame({
                "Categoría": ["Gastos Fijos (50%)", "Gastos Variables (20%)", "Ahorro (10%)", "Fondo/Inversión (10%)", "Excedente Libre (10%)"],
                "Presupuesto Meta": [gastos_fijos, var_e, ahorro_e, fondo_e, excedente_e]
            })
            df_e["Presupuesto Meta"] = df_e["Presupuesto Meta"].apply(lambda x: f"$ {x:,.2f}")
            st.table(df_e)
