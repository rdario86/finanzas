import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Diagnóstico Financiero", page_icon="📊", layout="wide")

# ==========================================================
# FUNCIÓN PARA GENERAR EL REPORTE EN PDF
# ==========================================================
def crear_pdf(ingresos, gastos_fijos, pct_fijos, estado, recomendacion, ingreso_req_aceptable=None, ingreso_req_excelente=None):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Diagnostico Financiero - Resultados', 0, 1, 'C')
            self.set_font('Arial', 'I', 10)

    pdf = PDF()
    pdf.add_page()
    
    def normalizar(texto):
        return texto.encode('latin-1', 'replace').decode('latin-1')

    # SECCIÓN 1: Resultados Actuales
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, normalizar('1. Tu Diagnóstico Actual'), 0, 1)
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, normalizar(f'Ingresos Totales: ${ingresos:,.2f}'), 0, 1)
    pdf.cell(0, 8, normalizar(f'Gastos Fijos Totales: ${gastos_fijos:,.2f}'), 0, 1)
    pdf.cell(0, 8, normalizar(f'Peso de tus Gastos Fijos: {pct_fijos:.1f}%'), 0, 1)
    pdf.ln(5)
    
    # SECCIÓN 2: Estatus y Recomendación
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, normalizar(f'ESTATUS: {estado}'), 0, 1)
    
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 8, normalizar(f'Recomendación: {recomendacion}'))
    pdf.ln(5)
    
    # SECCIÓN 3: Plan de Acción (Metas)
    if estado != "EXCELENTE":
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, normalizar('2. Plan de Acción: Metas de Ingreso'), 0, 1)
        pdf.ln(2)
        
        if estado in ["CRÍTICO", "CRÍTICO EXTREMO"] and ingreso_req_aceptable is not None:
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 8, normalizar('Meta ACEPTABLE (Fijos al 60%)'), 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 8, normalizar(f'Ingreso Mínimo Requerido: ${ingreso_req_aceptable:,.2f}'), 0, 1)
            
            pdf.cell(0, 8, normalizar(f' - Gastos Fijos (60%): ${gastos_fijos:,.2f}'), 0, 1)
            pdf.cell(0, 8, normalizar(f' - Gastos Variables (20%): ${(ingreso_req_aceptable*0.20):,.2f}'), 0, 1)
            pdf.cell(0, 8, normalizar(f' - Ahorro (10%): ${(ingreso_req_aceptable*0.10):,.2f}'), 0, 1)
            pdf.cell(0, 8, normalizar(f' - Inversión (10%): ${(ingreso_req_aceptable*0.10):,.2f}'), 0, 1)
            pdf.ln(5)
        
        if ingreso_req_excelente is not None:
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(0, 8, normalizar('Meta EXCELENTE (Fijos al 50%)'), 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 8, normalizar(f'Ingreso Mínimo Requerido: ${ingreso_req_excelente:,.2f}'), 0, 1)
            
            pdf.cell(0, 8, normalizar(f' - Gastos Fijos (50%): ${gastos_fijos:,.2f}'), 0, 1)
            pdf.cell(0, 8, normalizar(f' - Gastos Variables (20%): ${(ingreso_req_excelente*0.20):,.2f}'), 0, 1)
            pdf.cell(0, 8, normalizar(f' - Ahorro (10%): ${(ingreso_req_excelente*0.10):,.2f}'), 0, 1)
            pdf.cell(0, 8, normalizar(f' - Inversión (10%): ${(ingreso_req_excelente*0.10):,.2f}'), 0, 1)
            pdf.cell(0, 8, normalizar(f' - Excedente Libre (10%): ${(ingreso_req_excelente*0.10):,.2f}'), 0, 1)
            pdf.ln(5)

    # SECCIÓN 4: Nota sobre Deudas
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, normalizar('📌 Nota Importante sobre Deudas:'), 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, normalizar('De existir deudas, las mismas deben ser atacadas de forma prioritaria utilizando cualquier excedente libre, así como los fondos destinados a inversión, ahorro y recortando los gastos variables, hasta sanearlas por completo.'))
            
    # CORRECCIÓN DE COMPATIBILIDAD FPDF / FPDF2
    salida = pdf.output(dest='S')
    if isinstance(salida, str):
        return salida.encode('latin-1')
    else:
        return bytes(salida)

# ==========================================================
# INTERFAZ DE USUARIO (STREAMLIT)
# ==========================================================

st.title("Diagnóstico Financiero 📊")
st.markdown("#### Panel de Control - Rubén Núñez")
st.markdown("Ingresa tus ingresos y tus gastos fijos para evaluar tu estructura y calcular tu meta de ingresos ideal.")

with st.expander("ℹ️ Regla de Evaluación: El peso de tus Gastos Fijos"):
    st.markdown("""
    La salud de tu estructura se mide por el porcentaje que consumen tus **Gastos Fijos** sobre tus **Ingresos Totales**:
    
    - 🟢 **EXCELENTE:** < 50%
    - 🟡 **ACEPTABLE:** >= 50% y <= 60%
    - 🔴 **CRÍTICO:** > 60% (Y *CRÍTICO EXTREMO* si tus fijos superan el 100% de lo que ganas).
    """)

st.divider()

st.header("1. Ingresa tus datos mensuales")

col1, col2 = st.columns(2)
with col1:
    ingresos = st.number_input("Ingresos Totales (\$)", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
with col2:
    gastos_fijos = st.number_input("Gastos Fijos Totales (\$)", min_value=0.0, value=650.0, step=50.0, format="%.2f")

# INICIALIZAR LA MEMORIA
if 'diagnostico_generado' not in st.session_state:
    st.session_state.diagnostico_generado = False

# BOTÓN PARA GENERAR
if st.button("Generar Diagnóstico", type="primary"):
    if ingresos == 0:
        st.error("Los ingresos deben ser mayores a $0 para realizar el cálculo.")
        st.session_state.diagnostico_generado = False
    elif gastos_fijos == 0:
        st.error("Por favor, ingresa un monto válido para tus Gastos Fijos.")
        st.session_state.diagnostico_generado = False
    else:
        st.session_state.diagnostico_generado = True

# SI LA MEMORIA ESTÁ ACTIVADA, MOSTRAMOS LOS RESULTADOS
if st.session_state.diagnostico_generado:
    st.divider()
    st.header("2. Tu Diagnóstico Actual")
    
    pct_fijos = (gastos_fijos / ingresos) * 100
    
    ingreso_req_aceptable = None
    ingreso_req_excelente = gastos_fijos / 0.50
    
    if pct_fijos >= 100:
        estado = "CRÍTICO EXTREMO"
        color = "#8b0000"
        mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tus ingresos. ¡Tus compromisos fijos superan o igualan tu sueldo!"
        recomendacion = "🚨 Emergencia: Estás en bancarrota técnica, asumiendo deudas solo para existir. Debes hacer recortes drásticos a tu estilo de vida base inmediatamente."
        
    elif pct_fijos > 60:
        estado = "CRÍTICO"
        color = "#dc3545"
        mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tus ingresos. Estás por encima del límite de riesgo (> 60%)."
        recomendacion = "⚠️ Recomendación: Tu estilo de vida base es demasiado costoso para tu nivel de ingresos actual. Revisa las metas de ingresos requeridos más abajo."
        
    elif pct_fijos >= 50 and pct_fijos <= 60:
        estado = "ACEPTABLE"
        color = "#ffc107"
        mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tus ingresos. Te mantienes en la zona de equilibrio (>= 50% y <= 60%)."
        recomendacion = "✅ Recomendación: Tienes una estructura sana. Vigila que tus gastos fijos no suban y revisa abajo tu meta para pasar al siguiente nivel (EXCELENTE)."
        
    elif pct_fijos < 50:
        estado = "EXCELENTE"
        color = "#28a745"
        mensaje = f"Tus Gastos Fijos consumen el **{pct_fijos:.1f}%** de tus ingresos. Tienes una flexibilidad financiera sobresaliente (< 50%)."
        recomendacion = "🌟 Recomendación: Tu estructura es robusta. Mantén tus gastos fijos controlados para maximizar tu capacidad de construir patrimonio. ¡Sigue así!"

    st.markdown(f"Estatus de tu estructura: <strong style='color:{color}; font-size: 1.5em;'>{estado}</strong>", unsafe_allow_html=True)
    st.markdown(mensaje)
    st.markdown(f"**{recomendacion}**")
    
    if estado != "EXCELENTE":
        st.divider()
        st.header("3. Plan de Acción: Metas de Ingreso")
        
        if estado in ["CRÍTICO", "CRÍTICO EXTREMO"]:
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
                
                df_ace = pd.DataFrame({
                    "Distribución Ideal": ["Gastos Fijos (60%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)"],
                    "Monto Meta": [gastos_fijos, ingreso_req_aceptable*0.20, ingreso_req_aceptable*0.10, ingreso_req_aceptable*0.10]
                })
                df_ace["Monto Meta"] = df_ace["Monto Meta"].apply(lambda x: f"$ {x:,.2f}")
                st.table(df_ace)

            with col_b:
                st.markdown(f"### 🟢 Meta EXCELENTE")
                st.write("Para que tus fijos representen el **50%**, tu ingreso mínimo requerido debe ser:")
                st.markdown(f"<h3 style='color:#28a745;'>$ {ingreso_req_excelente:,.2f}</h3>", unsafe_allow_html=True)
                
                dif_exc = ingresos - ingreso_req_excelente
                if dif_exc > 0:
                    st.success(f"✅ Tus ingresos actuales superan esta meta por **\$ {dif_exc:,.2f}**.")
                elif dif_exc < 0:
                    st.warning(f"⚠️ Te faltan **\$ {abs(dif_exc):,.2f}** mensuales para alcanzar esta meta.")
                
                df_exc = pd.DataFrame({
                    "Distribución Ideal": ["Gastos Fijos (50%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)", "Excedente Libre (10%)"],
                    "Monto Meta": [gastos_fijos, ingreso_req_excelente*0.20, ingreso_req_excelente*0.10, ingreso_req_excelente*0.10, ingreso_req_excelente*0.10]
                })
                df_exc["Monto Meta"] = df_exc["Monto Meta"].apply(lambda x: f"$ {x:,.2f}")
                st.table(df_exc)

        elif estado == "ACEPTABLE":
            st.markdown("Tomando tus Gastos Fijos actuales de **\$ {:,.2f}** como un ancla inamovible, este es el ingreso mínimo requerido para llevar tu estructura al nivel óptimo:".format(gastos_fijos))
            
            col1_acep, col2_acep = st.columns([1.5, 1])
            with col1_acep:
                st.markdown(f"### 🟢 Meta para pasar a EXCELENTE")
                st.write("Para dar el siguiente paso y que tus fijos representen el **50%**, tu ingreso mínimo requerido debe ser:")
                st.markdown(f"<h3 style='color:#28a745;'>$ {ingreso_req_excelente:,.2f}</h3>", unsafe_allow_html=True)
                
                dif_exc = ingresos - ingreso_req_excelente
                if dif_exc < 0:
                    st.warning(f"⚠️ Te faltan **\$ {abs(dif_exc):,.2f}** mensuales para alcanzar esta meta.")
                else:
                    st.info("🎯 Tus ingresos actuales están exactamente en esta meta.")
                
                df_exc = pd.DataFrame({
                    "Distribución Ideal": ["Gastos Fijos (50%)", "Variables (20%)", "Ahorro (10%)", "Inversión (10%)", "Excedente Libre (10%)"],
                    "Monto Meta": [gastos_fijos, ingreso_req_excelente*0.20, ingreso_req_excelente*0.10, ingreso_req_excelente*0.10, ingreso_req_excelente*0.10]
                })
                df_exc["Monto Meta"] = df_exc["Monto Meta"].apply(lambda x: f"$ {x:,.2f}")
                st.table(df_exc)

    st.divider()
    
    st.subheader("📥 Llévate tu diagnóstico")
    st.write("Descarga un reporte profesional en PDF con tus resultados y estructura ideal.")
    
    # Generar los bytes del PDF
    pdf_bytes = crear_pdf(
        ingresos=ingresos,
        gastos_fijos=gastos_fijos,
        pct_fijos=pct_fijos,
        estado=estado,
        recomendacion=recomendacion,
        ingreso_req_aceptable=ingreso_req_aceptable,
        ingreso_req_excelente=ingreso_req_excelente
    )

    st.download_button(
        label="📄 Descargar Reporte PDF",
        data=pdf_bytes,
        file_name="Diagnostico_Financiero.pdf",
        mime="application/pdf"
    )
