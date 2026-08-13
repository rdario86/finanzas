import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Calculadora Bola de Nieve", layout="wide")

st.title("🧮 Calculadora de Deudas: Método Bola de Nieve")
st.write("Esta aplicación proyecta el pago de tus deudas priorizando desde la más pequeña a la más grande, acelerando el proceso al reinvertir los pagos liberados.")

# Barra lateral para parámetros globales
st.sidebar.header("Parámetros Generales")
ingresos = st.sidebar.number_input("Ingresos Totales", value=1860.0, step=100.0)
presupuesto_mensual = st.sidebar.number_input("Monto destinado al pago de deudas", value=558.0, step=10.0)
porcentaje_minimo = st.sidebar.number_input("% Pago Mínimo de deudas", value=4.0, step=0.1) / 100.0

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
            historial_excedentes = [] # Nuevo historial para rastrear el uso del excedente
            mes = 1
            limite_meses = 240 
            
            while np.sum(saldos) > 0 and mes <= limite_meses:
                dinero_disponible = presupuesto_mensual
                pagos_del_mes = np.zeros(n_deudas)
                excedentes_del_mes = np.zeros(n_deudas) # Excedente usado este mes por deuda
                
                # 1. Pago mínimo de deudas activas
                for i in range(n_deudas):
                    if saldos[i] > 0:
                        pago = min(pagos_minimos_fijos[i], saldos[i])
                        pagos_del_mes[i] = pago
                        dinero_disponible -= pago
                
                # 2. Asignación del excedente a la deuda más pequeña
                for i in range(n_deudas):
                    if saldos[i] > 0 and dinero_disponible > 0:
                        saldo_restante = saldos[i] - pagos_del_mes[i]
                        pago_extra = min(saldo_restante, dinero_disponible)
                        pagos_del_mes[i] += pago_extra
                        excedentes_del_mes[i] = pago_extra # Guardamos cuánto de la bola de nieve se usó aquí
                        dinero_disponible -= pago_extra
                        
                saldos = saldos - pagos_del_mes
                historial_saldos.append(saldos.copy())
                historial_excedentes.append(excedentes_del_mes.copy())
                mes += 1
                
            columnas_meses = [f"MES {i+1}" for i in range(len(historial_saldos))]
            
            # DataFrame principal de saldos
            df_historial = pd.DataFrame(historial_saldos).T
            df_historial.columns = columnas_meses
            
            # DataFrame secundario de excedentes (para los tooltips)
            df_historial_excedentes = pd.DataFrame(historial_excedentes).T
            df_historial_excedentes.columns = columnas_meses
            
            df_resultado = df_deudas[["Deuda", "Monto Inicial", "Pago Mínimo"]].copy()
            df_resultado = pd.concat([df_resultado, df_historial], axis=1)
            
            # 3. Creación de la matriz de Tooltips
            # Debe tener exactamente el mismo tamaño e índices que df_resultado
            df_tooltips = pd.DataFrame("", index=df_resultado.index, columns=df_resultado.columns)
            
            # Llenamos los tooltips solo para las columnas de los meses
            for col in columnas_meses:
                # Si se inyectó excedente, muestra el mensaje, si no, lo deja vacío
                df_tooltips[col] = df_historial_excedentes[col].apply(
                    lambda x: f"Excedente aplicado: ${x:,.2f}" if x > 0 else ""
                )
            
            # 4. Formatear la tabla final y aplicar los tooltips
            formato_moneda = {col: "${:,.2f}" for col in df_resultado.columns if col != "Deuda"}
            
            # Aplicamos el formato de moneda y seteamos la matriz de tooltips
            estilo_final = df_resultado.style.format(formato_moneda).set_tooltips(df_tooltips)
            
            st.subheader("Proyección de Pagos (Saldos al final de cada mes)")
            st.write("*(Pasa el cursor sobre los meses para ver el excedente aplicado a cada deuda)*")
            
            # SOLUCIÓN: Renderizamos la tabla estilizada como HTML puro para evitar que se vean las etiquetas <span>
            st.markdown(estilo_final.to_html(), unsafe_allow_html=True)
            
            st.info(f"¡Felicidades! Manteniendo esta disciplina, lograrás liquidar todas estas deudas en **{len(historial_saldos)} meses**.")
