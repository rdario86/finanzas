import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF

# Configuración de la página
st.set_page_config(page_title="Calculadora Bola de Nieve", layout="wide")

# ==========================================================
# FUNCIÓN PARA GENERAR EL REPORTE EN PDF (USANDO FPDF)
# ==========================================================
def crear_pdf(presupuesto_mensual, monto_minimo_total, df_resultado, df_historial_excedentes, num_meses):
    class PDF(FPDF):
        def header(self):
            # Cabecera Corporativa
            self.set_font('Arial', 'B', 14)
            self.set_text_color(0, 51, 102) # Azul oscuro
            self.cell(0, 10, 'REPORTE DE PLAN DE PAGOS - BOLA DE NIEVE', 0, 1, 'C')
            self.line(10, 20, 287, 20)
            self.ln(5)

        def footer(self):
            # Pie de página
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

    # Orientación Horizontal (Landscape) en A4 (297mm de ancho útil)
    pdf = PDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()

    # Función limpiadora de texto segura para FPDF
    def limpiar(texto):
        return str(texto).encode('latin-1', 'ignore').decode('latin-1')

    # --- SECCIÓN 1: RESUMEN DE PARÁMETROS ---
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 8, limpiar('1. Resumen de Presupuesto y Estrategia'), 0, 1)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 10)
    
    col_w = 135
    deuda_total_pdf = df_resultado['Monto Inicial'].sum()
    excedente_ini = presupuesto_mensual - monto_minimo_total
    
    # Inclusión del Monto Total de Deudas al inicio del resumen
    pdf.cell(col_w, 6, limpiar(f'Monto Total de Deudas: ${deuda_total_pdf:,.2f}'), 0, 0)
    pdf.cell(col_w, 6, limpiar(f'Monto Destinado a Deudas: ${presupuesto_mensual:,.2f}'), 0, 1)
    
    pdf.cell(col_w, 6, limpiar(f'Monto Pagos Minimos: ${monto_minimo_total:,.2f}'), 0, 0)
    pdf.cell(col_w, 6, limpiar(f'Bola de Nieve Inicial: ${excedente_ini:,.2f}'), 0, 1)
    
    pdf.cell(col_w, 6, limpiar(f'Tiempo Estimado de Pago: {num_meses} meses'), 0, 1)
    pdf.ln(4)

    # --- SECCIÓN 2: TABLA DE PROYECCIÓN ---
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 8, limpiar('2. Proyeccion de Pagos Mes a Mes'), 0, 1)

    # Cálculo dinámico del ancho de columnas para encajar en 277 mm de espacio impreso
    num_cols = len(df_resultado.columns)
    w_deuda = max(25.0, 277.0 / (num_cols + 1))
    w_col = (277.0 - w_deuda) / (num_cols - 1)
    
    # Encabezados de la Tabla
    pdf.set_font('Arial', 'B', 7)
    pdf.set_fill_color(240, 242, 246)
    pdf.set_text_color(49, 51, 63)
    
    for i, col in enumerate(df_resultado.columns):
        w = w_deuda if i == 0 else w_col
        align = 'L' if i == 0 else 'R'
        pdf.cell(w, 6, limpiar(col), 1, 0, align, fill=True)
    pdf.ln()

    # Filas de deudas
    pdf.set_font('Arial', '', 7)
    pdf.set_text_color(0, 0, 0)
    
    columnas_meses = [c for c in df_resultado.columns if c.startswith("MES ")]

    for idx, row in df_resultado.iterrows():
        for i, col in enumerate(df_resultado.columns):
            w = w_deuda if i == 0 else w_col
            align = 'L' if i == 0 else 'R'
            val = row[col]
            if col == 'Deuda':
                pdf.set_font('Arial', 'B', 7)
                pdf.cell(w, 5, limpiar(str(val)), 1, 0, align)
                pdf.set_font('Arial', '', 7)
            elif col in ['Monto Inicial', 'Pago Mínimo']:
                pdf.cell(w, 5, limpiar(f'${val:,.2f}'), 1, 0, align)
            else:
                exc_val = df_historial_excedentes.loc[idx, col] if col in df_historial_excedentes.columns else 0
                if exc_val > 0:
                    pdf.set_fill_color(232, 244, 253) # Azul claro para destacar inyección de excedente
                    pdf.cell(w, 5, limpiar(f'${val:,.2f}'), 1, 0, align, fill=True)
                else:
                    pdf.cell(w, 5, limpiar(f'${val:,.2f}'), 1, 0, align)
        pdf.ln()

    # Fila TOTAL SALDOS
    pdf.set_font('Arial', 'B', 7)
    pdf.set_fill_color(240, 242, 246)
    pdf.set_text_color(49, 51, 63)
    pdf.cell(w_deuda, 6, limpiar('TOTAL SALDOS'), 1, 0, 'L', fill=True)
    pdf.cell(w_col, 6, limpiar(f"${df_resultado['Monto Inicial'].sum():,.2f}"), 1, 0, 'R', fill=True)
    pdf.cell(w_col, 6, limpiar(f"${df_resultado['Pago Mínimo'].sum():,.2f}"), 1, 0, 'R', fill=True)
    for col in columnas_meses:
        pdf.cell(w_col, 6, limpiar(f"${df_resultado[col].sum():,.2f}"), 1, 0, 'R', fill=True)
    pdf.ln()

    # Fila EXCEDENTE APLICADO
    pdf.set_fill_color(232, 244, 253)
    pdf.set_text_color(0, 86, 179)
    pdf.cell(w_deuda, 6, limpiar('EXCEDENTE APLICADO'), 1, 0, 'L', fill=True)
    pdf.cell(w_col, 6, limpiar('-'), 1, 0, 'C', fill=True)
    pdf.cell(w_col, 6, limpiar('-'), 1, 0, 'C', fill=True)
    for col in columnas_meses:
        tot_exc = df_historial_excedentes[col].sum()
        pdf.cell(w_col, 6, limpiar(f"${tot_exc:,.2f}"), 1, 0, 'R', fill=True)
    pdf.ln()

    # Salida de bytes segura
    salida = pdf.output(dest='S')
    if isinstance(salida, str):
        return salida.encode('latin-1', 'ignore')
    else:
        return bytes(salida)

# ==========================================================
# INTERFAZ DE USUARIO (STREAMLIT)
# ==========================================================

st.title("🧮 Calculadora de Deudas: Método Bola de Nieve")
st.write("Esta aplicación proyecta el pago de tus deudas priorizando desde la más pequeña a la más grande, acelerando el proceso al reinvertir los pagos liberados.")

# --- BARRA LATERAL ---
st.sidebar.header("Parámetros Generales")

presupuesto_mensual = st.sidebar.number_input(
    "Monto destinado al pago de deudas", 
    value=558.0,
    step=10.0,
    help="Ingresa el monto mensual que destinarás a saldar deudas (no puede ser mayor a la deuda total)."
)

monto_minimo_total = st.sidebar.number_input(
    "Monto Total de Pagos Mínimos", 
    value=182.0, 
    step=10.0,
    help="Ingresa la suma de los pagos mínimos obligatorios de todas tus deudas."
)

if presupuesto_mensual > 0:
    porcentaje_representado = (monto_minimo_total / presupuesto_mensual) * 100
else:
    porcentaje_representado = 0.0

st.sidebar.caption(f"Representa el **{porcentaje_representado:.1f}%** del monto destinado a deudas.")
# ---------------------

# Resumen del presupuesto
st.write(f"Tu presupuesto mensual fijo para el pago de deudas es de **\${presupuesto_mensual:,.2f}**.")

st.subheader("Ingresa tus Deudas")
default_debts = pd.DataFrame({
    "Deuda": ["Deuda #1", "Deuda #2", "Deuda #3", "Deuda #4", "Deuda #5"],
    "Monto Inicial": [250.0, 300.0, 1000.0, 1000.0, 2000.0]
})

edited_debts = st.data_editor(default_debts, num_rows="dynamic", use_container_width=True)

# SUMATORIA EN TIEMPO REAL: Se calcula automáticamente al editar las filas
total_deudas_ingresadas = edited_debts["Monto Inicial"].fillna(0).sum()
st.metric(label="💰 Total Deuda Acumulada", value=f"${total_deudas_ingresadas:,.2f}")

if st.button("Calcular Plan de Pagos", type="primary"):
    df_deudas = edited_debts[edited_debts["Monto Inicial"] > 0].copy()
    
    if df_deudas.empty:
        st.warning("Por favor, ingresa al menos una deuda con un monto mayor a 0.")
    else:
        df_deudas = df_deudas.sort_values(by="Monto Inicial").reset_index(drop=True)
        suma_total_deudas = df_deudas["Monto Inicial"].sum()
        
        # VALIDACIÓN: El presupuesto destinado no puede ser mayor que el total de las deudas
        if presupuesto_mensual > suma_total_deudas:
            st.error(
                f"El monto destinado al pago de deudas (**\${presupuesto_mensual:,.2f}**) no puede ser mayor "
                f"al monto total de tus deudas (**\${suma_total_deudas:,.2f}**). Por favor ajusta el valor en el menú lateral."
            )
        else:
            df_deudas["Pago Mínimo"] = (df_deudas["Monto Inicial"] / suma_total_deudas) * monto_minimo_total
            total_pago_minimo = df_deudas["Pago Mínimo"].sum()
            
            if presupuesto_mensual < total_pago_minimo:
                st.error(f"Tu presupuesto mensual (**\${presupuesto_mensual:,.2f}**) es menor al pago mínimo requerido (**\${total_pago_minimo:,.2f}**). Necesitas aumentar el monto destinado.")
            else:
                excedente_inicial = presupuesto_mensual - total_pago_minimo
                st.success(f"Tus pagos mínimos suman **\${total_pago_minimo:,.2f}**. Tienes un excedente (Bola de Nieve) de **\${excedente_inicial:,.2f}** para acelerar los pagos en el primer mes.")
                
                saldos = df_deudas["Monto Inicial"].values.copy()
                pagos_minimos_fijos = df_deudas["Pago Mínimo"].values.copy()
                n_deudas = len(saldos)
                
                historial_saldos = []
                historial_excedentes = [] 
                mes = 1
                limite_meses = 240 
                
                while np.sum(saldos) > 0 and mes <= limite_meses:
                    dinero_disponible = presupuesto_mensual
                    pagos_del_mes = np.zeros(n_deudas)
                    excedentes_del_mes = np.zeros(n_deudas)
                    
                    for i in range(n_deudas):
                        if saldos[i] > 0:
                            pago = min(pagos_minimos_fijos[i], saldos[i])
                            pagos_del_mes[i] = pago
                            dinero_disponible -= pago
                    
                    for i in range(n_deudas):
                        if saldos[i] > 0 and dinero_disponible > 0:
                            saldo_restante = saldos[i] - pagos_del_mes[i]
                            pago_extra = min(saldo_restante, dinero_disponible)
                            pagos_del_mes[i] += pago_extra
                            excedentes_del_mes[i] = pago_extra 
                            dinero_disponible -= pago_extra
                            
                    saldos = saldos - pagos_del_mes
                    historial_saldos.append(saldos.copy())
                    historial_excedentes.append(excedentes_del_mes.copy())
                    mes += 1
                    
                columnas_meses = [f"MES {i+1}" for i in range(len(historial_saldos))]
                
                df_historial = pd.DataFrame(historial_saldos).T
                df_historial.columns = columnas_meses
                
                df_historial_excedentes = pd.DataFrame(historial_excedentes).T
                df_historial_
