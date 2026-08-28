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
    
    col_w = 130
    excedente_ini = presupuesto_mensual - monto_minimo_total
    
    pdf.cell(col_w, 6, limpiar(f'Monto Destinado a Deudas: ${presupuesto_mensual:,.2f}'), 0, 0)
    pdf.cell(col_w, 6, limpiar(f'Monto Pagos Minimos: ${monto_minimo_total:,.2f}'), 0, 1)
    
    pdf.cell(col_w, 6, limpiar(f'Bola de Nieve Inicial: ${excedente_ini:,.2f}'), 0, 0)
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
