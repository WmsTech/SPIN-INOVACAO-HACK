import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import numpy as np

# Definindo o nome da guia do navegador
st.set_page_config(page_title="Monitoramento Preditivo - Motor", page_icon="⚙️", layout="wide")

# Carregar o Modelo
@st.cache_resource
def carregar_modelo():
    try:
        return joblib.load('modelo_rf_motor_rf.pkl')
    except:
        return None

modelo = carregar_modelo()

# Crianção do Layout da Pagina, para isso feita em blocos

# Criação do cabeçalho da Pagina
st.title("⚙️ PreditIA - Sistema Inteligente de Manutenção Preditiva")
st.markdown("Monitoramento de Motor de Indução Trifásico utilizando Machine Learning para predição de falhas.")

# 4. Barra Lateral - Vai ser um simulador para os sensores
st.sidebar.header("🎛️ Simulador de Sensores")
st.sidebar.markdown("Ajuste os valores para testar a IA.")

temp_input = st.sidebar.slider("Temperatura do Estator (°C)", min_value=20.0, max_value=150.0, value=70.0, step=0.5)
vib_input = st.sidebar.slider("Vibração (mm/s)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
corr_input = st.sidebar.slider("Corrente Elétrica (A)", min_value=0.0, max_value=30.0, value=12.0, step=0.5)


tab1, = st.tabs(["📊 Monitoramento em Tempo Real"])

# Montando um Dashboard
with tab1:
    
    # Simulando as diferenças verificadas pelo sistema 
    # Aplicação apenas de exemplo
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperatura Atual", f"{temp_input} °C", delta="+1.5 °C (Última hora)", delta_color="inverse")
    col2.metric("Nível de Vibração", f"{vib_input} mm/s", delta="+0.2 mm/s", delta_color="inverse")
    col3.metric("Corrente Elétrica", f"{corr_input} A", delta="-0.5 A", delta_color="normal")
    
    st.divider()

    # Gráficos 
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        fig_temp = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = temp_input,
            title = {'text': "Temperatura (°C)", 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [0, 150]},
                'bar': {'color': "rgba(0,0,0,0.5)"},
                'steps': [
                    {'range': [0, 80], 'color': "#2ecc71"},   
                    {'range': [80, 95], 'color': "#f1c40f"},  
                    {'range': [95, 150], 'color': "#e74c3c"}  
                ]
            }
        ))
        fig_temp.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_temp, use_container_width=True)

    with col_g2:
        fig_vib = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = vib_input,
            title = {'text': "Vibração (mm/s)", 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [0, 20]},
                'bar': {'color': "rgba(0,0,0,0.5)"},
                'steps': [
                    {'range': [0, 3.5], 'color': "#2ecc71"},
                    {'range': [3.5, 6.5], 'color': "#f1c40f"},
                    {'range': [6.5, 20], 'color': "#e74c3c"}
                ]
            }
        ))
        fig_vib.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_vib, use_container_width=True)

    st.divider()


# Definição de Status para a determinação de Manutenção preditiva.
# COm a porcentagem é possivel através de integração com outro sistema acionar a equipe de manutenção
if modelo is not None:
    dados_entrada = pd.DataFrame({'Temperatura_C': [temp_input], 'Vibracao_mms': [vib_input], 'Corrente_A': [corr_input]})
    
    probabilidades = modelo.predict_proba(dados_entrada)[0]
    predicao = modelo.classes_[np.argmax(probabilidades)]
    certeza = max(probabilidades) * 100

    if predicao == 'Saudavel':
        st.success(f"✅ **STATUS: SAUDÁVEL** (Certeza: {certeza:.1f}%)")
    elif predicao == 'Alerta':
        st.warning(f"⚠️ **STATUS: ALERTA** (Certeza: {certeza:.1f}%)")
    else:
        st.error(f"🚨 **STATUS: FALHA IMINENTE** (Certeza: {certeza:.1f}%)")