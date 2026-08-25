import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Calculadora Bola de Nieve", layout="wide")

st.title("🧮 Calculadora de Deudas: Método Bola de Nieve")
st.write("Esta aplicación proyecta el pago de tus deudas priorizando desde la más pequeña a la más grande, acelerando el proceso al reinvertir los pagos liberados.")

# --- BARRA LATERAL ---
st.sidebar.header("Parámetros Generales")
ingresos = st.sidebar.number_input("Ingresos Totales", value=1860.0, step=100.0)

# 1. Calculamos el límite estricto del 30% de los ingresos
limite_presupuesto = ingresos * 0.30

# 2. Aseguramos que el valor inicial (558.0) no sea mayor al límite para evitar errores de Streamlit
valor_inicial = min(558.0, limite_presupuesto)

# 3. Agregamos max_value y un tooltip de ayuda (help)
presupuesto_mensual = st.sidebar.number_input(
    "Monto destinado al pago de deudas", 
    value=float(valor_inicial), 
    max_value=float(limite_presupuesto), # Aquí aplicamos el tope del 30%
    step=10.0,
    help="Por recomendación financiera, este monto no puede superar el 30% de tus ingresos totales."
)

porcentaje_minimo = st.sidebar.number_input("% Pago Mínimo de deudas", value=4.0, step=0.1) / 100.0
# ---------------------

# Resumen del presupuesto
st.write(f"Con un ingreso total de **\${ingresos:,.2f}**, tu presupuesto mensual fijo para el pago de deudas es de **\${presupuesto_mensual:,.2f}**.")

st.subheader("Ingresa tus Deudas")
default_debts = pd.DataFrame({
    "Deuda": ["Deuda #1", "Deuda #2", "Deuda #3", "Deuda #4", "Deuda #5"],
    "Monto Inicial": [250.0, 300.0, 1000.0, 1000.0, 2000.0]
})

edited_debts = st.data_editor(default_debts, num_rows="dynamic", use_container_width=True)

if st.button("Calcular Plan de Pagos", type="primary"):
    df_deudas = edited_debts[edited_debts["Monto Inicial"] > 0].copy()
    
    if df_deudas.empty:
        st.warning("Por favor, ingresa al menos una deuda con un monto mayor a 0.")
    else:
        df_deudas = df_deudas.sort_values(by="Monto Inicial").reset_index(drop=True)
        df_deudas["Pago Mínimo"] = df_deudas["Monto Inicial"] * porcentaje_minimo
        total_pago_minimo = df_deudas["Pago Mínimo"].sum()
        
        if presupuesto_mensual < total_pago_minimo:
            st.error(f"Tu presupuesto mensual (**\${presupuesto_mensual:,.2f}**) es menor al pago mínimo requerido (**\${total_pago_minimo:,.2f}**). Necesitas aumentar el monto destinado o tus ingresos.")
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
            df_historial_excedentes.columns = columnas_meses
            
            df_resultado = df_deudas[["Deuda", "Monto Inicial", "Pago Mínimo"]].copy()
            df_resultado = pd.concat([df_resultado, df_historial], axis=1)
            
            st.subheader("Proyección de Pagos (Saldos al final de cada mes)")
            st.write("*(Pasa el cursor sobre los montos de los meses para ver el excedente aplicado)*")
            
            # Generación de tabla HTML personalizada
            html_tabla = '<div class="tabla-custom" style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 8px; padding: 15px; max-height: 450px;">\n'
            html_tabla += '<table style="width: 100%; border-collapse: collapse; font-size: 13px; font-family: sans-serif; color: inherit;">\n'
            
            html_tabla += '<thead>\n<tr style="background-color: #f0f2f6; border-bottom: 2px solid #ddd; color: #31333F;">\n'
            for col in df_resultado.columns:
                align = 'left' if col == 'Deuda' else 'right'
                html_tabla += f'<th style="padding: 8px 12px; text-align: {align};">{col}</th>\n'
            html_tabla += '</tr>\n</thead>\n'
            
            html_tabla += '<tbody>\n'
            for idx, row in df_resultado.iterrows():
                html_tabla += '<tr style="border-bottom: 1px solid #eee;">\n'
                for col in df_resultado.columns:
                    val = row[col]
                    if col == 'Deuda':
                        html_tabla += f'<td style="padding: 8px 12px; text-align: left; font-weight: bold;">{val}</td>\n'
                    elif col in ['Monto Inicial', 'Pago Mínimo']:
                        html_tabla += f'<td style="padding: 8px 12px; text-align: right;">${val:,.2f}</td>\n'
                    else:
                        exc_val = df_historial_excedentes.loc[idx, col] if col in df_historial_excedentes.columns else 0
                        if exc_val > 0:
                            tooltip_text = f"Excedente aplicado: ${exc_val:,.2f}"
                            html_tabla += f'<td style="padding: 8px 12px; text-align: right; cursor: help; background-color: rgba(24, 144, 255, 0.1);" title="{tooltip_text}">${val:,.2f}</td>\n'
                        else:
                            html_tabla += f'<td style="padding: 8px 12px; text-align: right;">${val:,.2f}</td>\n'
                html_tabla += '</tr>\n'
            html_tabla += '</tbody>\n</table>\n</div>'
            
            st.markdown(html_tabla, unsafe_allow_html=True)
            
            st.info(f"¡Felicidades! Manteniendo esta disciplina, lograrás liquidar todas estas deudas en **{len(historial_saldos)} meses**.")
