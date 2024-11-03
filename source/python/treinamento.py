import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Carregar os dados
df_treino = pd.read_csv('vitimas_treino.csv')
df_teste = pd.read_csv('vitimas_teste.csv')
df_serial_killers = pd.read_csv('serial_killers.csv')

# Apenas vítimas associadas serão usadas no treinamento
df_treino = df_treino[df_treino['Serial Killer'] != 'Desconhecido']

# Lista de serial killers
serial_killers = df_treino['Serial Killer'].unique()

# Características para plotar
features_num = ['Idade', 'Altura', 'Peso']
features_class = ['Sexo', 'Cor dos Olhos', 'Cor do Cabelo', 'Causa Morte', 'Local', 'Raça', 'Classe Social']
features_all = df_treino.columns[1:-1] # Todas as características exceto 'Serial Killer'

serial_killers_dic = {
   'Nome': [],
   'Sexo': [],  # F = Feminino, M = Masculino, A = Ambos
   'Idade': [],
   'Altura': [],
   'Peso': [],
   'Cor do Cabelo': [],
   'Cor dos Olhos': [],
   'Raça': [],
   'Causa Morte': [],  # Método de assassinato
   'Local': [],  # Local onde a vítima foi morta
   'Classe Social': []  # Classe social da vítima
}

def analise_geral(df, graficos):
   print("Análise Geral dos Dados")
   print("=" * 40)
    
   for killer in serial_killers:
      print(f"\nAnalisando o Serial Killer: {killer}")
      print("-" * 40)
        
      subset = df[df['Serial Killer'] == killer]
      
      serial_killers_dic['Nome'].append(killer)
        
      for coluna in features_all:
         # Calcular a média para características numéricas
         if coluna in features_num:
            mediana = subset[coluna].median()
            print(f"\nMediana para {coluna}: {mediana}")
            
            if (graficos):
               plt.figure(figsize=(10, 6))
               sns.kdeplot(subset[coluna], fill=True)
               plt.title(f'Distribuição de {coluna} - {killer}')
               plt.legend([f'Mediana: {mediana}'])
               plt.xlabel(coluna)
               plt.ylabel('Densidade')
               plt.show()
            
            serial_killers_dic[coluna].append(mediana)
         
         # Calcular a distribuição para características categóricas
         elif coluna in features_class:
            if subset[coluna].nunique() == 1:
               moda = subset[coluna].mode()[0]
               
            else:
               dif = abs(subset[coluna].value_counts().max() - subset[coluna].value_counts().min())
               if dif < subset[coluna].count() / (subset[coluna].nunique()):
                  moda = 'Todos'
                  
               else:
                  moda = subset[coluna].mode()[0]
            
            serial_killers_dic[coluna].append(moda) 
            print(f"\nDistribuição para {subset[coluna].value_counts()}")
            print(f"Valor mais comum: {moda}")
            
            if (graficos):
               plt.figure(figsize=(10, 6))
               sns.countplot(x=coluna, data=subset, palette='viridis', hue=coluna)
               plt.title(f'Distribuição de {coluna} - {killer}')
               plt.legend([f'Mais comum: {subset[coluna].mode()[0]}'])
               plt.xlabel(coluna)
               plt.ylabel('Contagem')
               plt.show()
            
         print("=" * 40)
         
# Função para comparar cada categoria de serial_killers_dic com df_serial_killers para cada serial killer
def comparar_serial_killers():
   for killer in serial_killers:
      print(f"\nComparando Serial Killer: {killer}")
      print("-" * 40)
      
      for coluna in features_all:
         
         print(f"\nPrevisão: {serial_killers_dic[coluna][-1]}")
         print(f"Real: {df_serial_killers[df_serial_killers['Nome'] == killer][coluna].values[0]}")
         
         if coluna in features_num:
            dif = abs(df_serial_killers[df_serial_killers['Nome'] == killer][coluna].values[0] - serial_killers_dic[coluna][-1])
               
            if coluna == 'Altura' and dif < 0.1:
               print(f"{coluna}: Correto")
            elif dif < 10:
               print(f"{coluna}: Correto")
            else:
               print(f"{coluna}: Incorreto")
               
            print(f"Diferença: {round(dif, 2)}")
         
         if coluna in features_class:
            if df_serial_killers[df_serial_killers['Nome'] == killer][coluna].values[0] == serial_killers_dic[coluna][-1]:
               print(f"{coluna}: Correto")
            else:
               print(f"{coluna}: Incorreto")
         print("=" * 40)

analise_geral(df_treino, 0)
comparar_serial_killers()

serial_killers_df = pd.DataFrame(serial_killers_dic)
serial_killers_df.to_csv("serial_killers_previstos.csv", index=True)
