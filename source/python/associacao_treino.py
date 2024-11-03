import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# Função que define qual serial killer matou uma vítima com base em suas preferências
# e atualiza o número de vítimas de cada serial killer
path_serial_killers = 'serial_killers.csv'
path_vitimas_treino = 'vitimas_treino.csv'

# Carregando os dados dos serial killers e das vítimas
serial_killers_df = pd.read_csv(path_serial_killers, index_col=0)
vitimas_treino_df = pd.read_csv(path_vitimas_treino, index_col=0)

quantidade_vitimas_treino = len(vitimas_treino_df)
quantidade_associacoes_treino = 0
quantidade_associacoes_teste = 0

# Função para associar uma vítima a um serial killer
def associar_vitima(vitima_id, vitimas_df):
   menor_peso = 99
   mais_provavel_id = 99
    
   for id in range(len(serial_killers_df)):
      peso = 0
      serial_killer = serial_killers_df.iloc[id]
      vitima = vitimas_df.iloc[vitima_id]
      
      if not serial_killer['Sexo'] in ['Todos', vitima['Sexo']]:
         peso += 5
         
      idade_dif = abs(serial_killer['Idade'] - vitima['Idade'])    
      if not idade_dif <= 3:
         if idade_dif > 7:
            peso += 5
         else:
            peso += 3
      
      tamanho_dif = abs(serial_killer['Altura'] - vitima['Altura'])
      if not tamanho_dif <= 0.07:
         if tamanho_dif > 0.10:
            peso += 5
         else:
            peso += 3
      
      peso_dif = abs(serial_killer['Peso'] - vitima['Peso'])
      if not peso_dif <= 3:
         if peso_dif > 7:
            peso += 5
         else:
            peso += 3
      
      if not serial_killer['Cor do Cabelo'] in ['Todos', vitima['Cor do Cabelo']]:
         peso += 2
         
      if not serial_killer['Cor dos Olhos'] in ['Todos', vitima['Cor dos Olhos']]:
         peso += 2   
         
      if not serial_killer['Raça'] in ['Todos', vitima['Raça']]:
         peso += 4
      
      if not serial_killer['Causa Morte'] in ['Todos', vitima['Causa Morte']]:
         peso += 5
         
      if not serial_killer['Local'] in ['Todos', vitima['Local']]:
         peso += 5
         
      if not serial_killer['Classe Social'] in ['Todos', vitima['Classe Social']]:
         peso += 3
         
      if peso <= menor_peso:
         menor_peso = peso
         mais_provavel_id = id
            
   if menor_peso > 7 or mais_provavel_id == 99:
      vitimas_df.at[vitima_id, 'Serial Killer'] = 'Desconhecido'
      return 0
    
   serial_killers_df.at[mais_provavel_id, 'Vítimas'] += 1
   vitimas_df.at[vitima_id, 'Serial Killer'] = serial_killers_df.iloc[mais_provavel_id]['Nome']
   return 1

# Resetando contagem de vítimas
for id in range(len(serial_killers_df)):
   serial_killers_df.at[id, 'Vítimas'] = 0

# Associando todas as vítimas
for id in range(quantidade_vitimas_treino):
   if associar_vitima(id, vitimas_treino_df):
      quantidade_associacoes_treino += 1
      
print(f'Foram associadas {quantidade_associacoes_treino} de {quantidade_vitimas_treino} vítimas (treino) a um serial killer.')

for id in range(len(serial_killers_df)):
   serial_killer = serial_killers_df.iloc[id]
   print(f'O serial killer {serial_killer["Nome"]} matou {serial_killer["Vítimas"]} vítimas.')

# Separando as vítimas associadas e não associadas
vitimas_associadas_treino_df = vitimas_treino_df[vitimas_treino_df['Serial Killer'] != 'Desconhecido']
vitimas_desconhecidas_treino_df = vitimas_treino_df[vitimas_treino_df['Serial Killer'] == 'Desconhecido']

print (f'Vítimas associadas treino: {len(vitimas_associadas_treino_df)}')
print (f'Vítimas desconhecidas (antes): {len(vitimas_desconhecidas_treino_df)}')

# Reduzindo o tamanho das vítimas não associadas para 10% das vítimas associadas
if len(vitimas_desconhecidas_treino_df) > len(vitimas_associadas_treino_df): 
   vitimas_desconhecidas_treino_df = vitimas_desconhecidas_treino_df.sample(frac=(0.2 * len(vitimas_associadas_treino_df) / len(vitimas_desconhecidas_treino_df)))

print (f'Vítimas desconhecidas treino (depois): {len(vitimas_desconhecidas_treino_df)}')

# Mesclando as vítimas associadas e não associadas
vitimas_treino_df = pd.concat([vitimas_associadas_treino_df, vitimas_associadas_treino_df, vitimas_desconhecidas_treino_df])

# Embaralhando a ordem das vítimas
vitimas_treino_df = vitimas_treino_df.sample(frac=1)

# Salvando os dados atualizados
serial_killers_df.to_csv(path_serial_killers, index=True)
vitimas_treino_df.to_csv(path_vitimas_treino, index=True)

print(f'Vitimas treino: {len(vitimas_treino_df)}')
print('Vítimas atualizadas com sucesso!')