import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Carregamento dos dados tratados
df = pd.read_csv('dados_limpos_motor.csv')

# Determinação das variaveis de treino e teste
X = df[['Temperatura_C', 'Vibracao_mms', 'Corrente_A']]
y = df['Status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Utilização da Randow Forest como modelo de IA
modelo_rf = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42, class_weight='balanced')
modelo_rf.fit(X_train, y_train)


# Criação do arquivo para o Front-End
joblib.dump(modelo_rf, 'modelo_rf_motor_rf.pkl')

# Metricas para avaliar treinamento
importances = dict(zip(X.columns, modelo_rf.feature_importances_))
print(f"Modelo_rf treinado. Acurácia: {modelo_rf.score(X_test, y_test):.2f}")
print(f"Importâncias: {importances}")