import pandas as pd
import numpy as np


# Realizando o carregamento do banco de dados gerados
df = pd.read_csv('dados_brutos.csv')
df_limpo = df.copy()

df.info()

# Realizando o tratamento do problema de tipo e uso de virgula, após obter informações do banco de dados.
df_limpo['Temperatura_C'] = pd.to_numeric(df_limpo['Temperatura_C'].astype(str).str.replace(',', '.'), errors='coerce')

# Limpeza de Outliers Físicos (Valores fisicamente irreais) sendo tranformados em NaN
df_limpo.loc[(df_limpo['Temperatura_C'] > 200) | (df_limpo['Temperatura_C'] < 0), 'Temperatura_C'] = np.nan
df_limpo.loc[df_limpo['Corrente_A'] < 0, 'Corrente_A'] = np.nan

# Preenchendo valores NaN com o valor anterior, ou o posterior caso a primeira linha seja NaN.
df_limpo = df_limpo.ffill().bfill()

df_limpo = df_limpo[(df_limpo['Temperatura_C'] > 0) & (df_limpo['Temperatura_C'] < 200)]
df_limpo = df_limpo[(df_limpo['Corrente_A'] > 0) & (df_limpo['Corrente_A'] < 100)] 


# Deteminação do Status para o treinamento
def classificar_estado(row):
    if row['Temperatura_C'] >= 130 or row['Vibracao_mms'] >= 4.5 or row['Corrente_A'] >= 17.25:
        return 'Falha'
    elif row['Temperatura_C'] >= 100 or row['Vibracao_mms'] >= 2.3 or row['Corrente_A'] >= 15:
        return 'Alerta'
    else:
        return 'Saudavel'

df_limpo['Status'] = df_limpo.apply(classificar_estado, axis=1)
df_limpo.sample(frac=1).to_csv('dados_limpos_motor.csv', index=False)
print("Tratamento de dados realizado. Data Frame pronto para o modelo de IA.")