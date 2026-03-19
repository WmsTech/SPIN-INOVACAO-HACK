import pandas as pd
import numpy as np

np.random.seed(42)
n = 500


# Criando a base de dados
# Está sendo utilizado uma distrivuição gausiana para simular uma coletar mais realista
# O objetivo é criar 3 "zonas de dados", que representam a zona de operação do motor
t1, v1, c1 = np.random.normal(65, 2, 500), np.random.normal(1.5, 0.2, 500), np.random.normal(12, 0.5, 500)
t2, v2, c2 = np.random.normal(85, 2, 500), np.random.normal(4.5, 0.3, 500), np.random.normal(16, 0.3, 500)
t3, v3, c3 = np.random.normal(115, 3, 500), np.random.normal(8.5, 0.5, 500), np.random.normal(22, 1, 500)
temp = np.concatenate([t1, t2, t3])
vibr = np.concatenate([v1, v2, v3])
corr = np.concatenate([c1, c2, c3])

df = pd.DataFrame({'Temperatura_C': temp, 'Vibracao_mms': vibr, 'Corrente_A': corr})

# Para simular um banco de dados mais fiel, foi adicionado alguns "ruidos" para serem tratados
# Essa injeção de ruido, são referente a ruido classicos de banco de dados
# Problema de tipo causado por virgula, Not a Number e valores fisicamente irreais
df.loc[df.sample(frac=0.1).index, 'Temperatura_C'] = "999,99" # String com vírgula e erro
df.loc[df.sample(frac=0.05).index, 'Vibracao_mms'] = np.nan
df.loc[df.sample(frac=0.02).index, 'Corrente_A'] = -10.0

df.to_csv('dados_brutos.csv', index=False)
print("Dados brutos gerados.")