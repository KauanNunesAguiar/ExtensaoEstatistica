import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# Função que define qual serial killer matou uma vítima com base em suas preferências
# e atualiza o número de vítimas de cada serial killer
path_serial_killers = 'serial_killers_previstos.csv'
path_vitimas_teste = 'vitimas_teste.csv'

# Carregando os dados dos serial killers e das vítimas
serial_killers_df = pd.read_csv(path_serial_killers, index_col=0)
vitimas_teste_df = pd.read_csv(path_vitimas_teste, index_col=0)

quantidade_vitimas_teste = len(vitimas_teste_df)
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
   
for id in range(quantidade_vitimas_teste):
   if associar_vitima(id, vitimas_teste_df):
      quantidade_associacoes_teste += 1
      
print(f'Foram associadas {quantidade_associacoes_teste} de {quantidade_vitimas_teste} vítimas (teste) a um serial killer.')

for id in range(len(serial_killers_df)):
   serial_killer = serial_killers_df.iloc[id]
   print(f'O serial killer {serial_killer["Nome"]} matou {serial_killer["Vítimas"]} vítimas.')

# Salvando os dados atualizados
serial_killers_df.to_csv(path_serial_killers, index=True)
vitimas_teste_df.to_csv(path_vitimas_teste, index=True)

print(f'Vitimas teste: {len(vitimas_teste_df)}')
print('Vítimas atualizadas com sucesso!')