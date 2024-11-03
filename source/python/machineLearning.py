import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

# Carregar os dados
df_treino = pd.read_csv('vitimas_treino.csv', index_col=0)
df_teste = pd.read_csv('vitimas_teste.csv', index_col=0)

# Características para plotar
features_num = ['Idade', 'Altura', 'Peso']
features_class = ['Sexo', 'Cor dos Olhos', 'Cor do Cabelo', 'Causa Morte', 'Local', 'Raça', 'Classe Social']
features_all = df_treino.columns[1:-1] # Todas as características exceto 'Serial Killer'

# Apenas vítimas associadas serão usadas no treinamento
vitimas_associadas_df = df_treino[df_treino['Serial Killer'] != 'Desconhecido']
vitimas_associadas_df = vitimas_associadas_df.dropna()

# Apenas vítimas associadas serão usadas no teste
df_teste = df_teste['Serial Killer'] != 'Desconhecido'
df_teste = df_teste.dropna()

# Transformar dados categóricos em numéricos com LabelEncoder
le = LabelEncoder()
for column in features_class:
   vitimas_associadas_df[column] = le.fit_transform(vitimas_associadas_df[column])
   df_teste[column] = le.fit_transform(df_teste[column])
   
# Normalizar os dados numéricos
scaler = StandardScaler()
for column in features_num:
   vitimas_associadas_df[column] = scaler.fit_transform(vitimas_associadas_df[column].values.reshape(-1, 1))
   df_teste[column] = scaler.fit_transform(df_teste[column].values.reshape(-1, 1))
   
# Selecionar as features (características das vítimas)
x = vitimas_associadas_df[['Sexo', 'Idade', 'Altura', 'Peso', 'Cor dos Olhos', 'Cor do Cabelo', 'Causa Morte', 'Local', 'Raça', 'Classe Social']]

# Variável alvo (o serial killer responsável)
y = vitimas_associadas_df['Serial Killer']

# Dividir o dataset em treino e teste (80% treino, 20% teste)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Criar o modelo de Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Treinar o modelo
model.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
y_pred = model.predict(X_test)

# Exibir relatório de classificação
print(classification_report(y_test, y_pred))

print('Treinamento concluído!')

# Fazer previsões no conjunto de teste
x_test2 = df_teste[['Sexo', 'Idade', 'Altura', 'Peso', 'Cor dos Olhos', 'Cor do Cabelo', 'Causa Morte', 'Local', 'Raça', 'Classe Social']]
y_test2 = df_teste['Serial Killer']
y_pred2 = model.predict(x_test2)

# Exibir relatório de classificação
print(classification_report(y_test2, y_pred2))
print('Teste concluído!')