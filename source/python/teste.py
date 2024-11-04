from bibliotecas import *

# Carregando os dados dos serial killers e das vítimas
serial_killers_df = pd.read_csv(path_serial_killers_previstos, index_col=0)
vitimas_teste_df = pd.read_csv(path_vitimas_teste, index_col=0)

quantidade_vitimas_treino = len(vitimas_teste_df)
quantidade_associacoes_treino = 0
quantidade_associacoes_teste = 0

def define_peso(serial_killer, vitima, caracteristica, peso_min, peso_max):
   if caracteristica in features_all:
      if caracteristica in caracteristicas_categorias:
         if serial_killer[caracteristica] == 'Todos':
            return peso_min
         
         elif not serial_killer[caracteristica] in [vitima[caracteristica]]:
            return peso_max
         
         return 0
         
      elif caracteristica in caracteristicas_numericas:
         diff = abs(serial_killer[caracteristica] - vitima[caracteristica])
         if not diff <= caracteristicas_numericas[caracteristica][2]:
            if diff >= caracteristicas_numericas[caracteristica][3]:
               return peso_max
            
            else:
               return peso_min
            
         return 0
      
      else:
         return 99

# Função para associar uma vítima a um serial killer
def associar_vitima(vitima_id, vitimas_df):
   menor_peso = 99
   mais_provavel_id = 99
    
   for id in range(len(serial_killers_df)):
      peso = 0
      serial_killer = serial_killers_df.iloc[id]
      vitima = vitimas_df.iloc[vitima_id]
      
      peso += define_peso(serial_killer, vitima, 'Sexo', 0, 5)
      peso += define_peso(serial_killer, vitima, 'Idade', 3, 5)
      peso += define_peso(serial_killer, vitima, 'Altura', 3, 5)
      peso += define_peso(serial_killer, vitima, 'Peso', 0, 5)
      peso += define_peso(serial_killer, vitima, 'Cor do Cabelo', 0, 2)
      peso += define_peso(serial_killer, vitima, 'Cor dos Olhos', 0, 2)
      peso += define_peso(serial_killer, vitima, 'Raça', 0, 4)
      peso += define_peso(serial_killer, vitima, 'Causa Morte', 0, 5)
      peso += define_peso(serial_killer, vitima, 'Local Morte', 0, 5)
      peso += define_peso(serial_killer, vitima, 'Classe Social', 0, 3)
         
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
   if associar_vitima(id, vitimas_teste_df):
      quantidade_associacoes_treino += 1
      
print(f'Foram associadas {quantidade_associacoes_treino} de {quantidade_vitimas_treino} vítimas a um serial killer.')

for id in range(len(serial_killers_df)):
   serial_killer = serial_killers_df.iloc[id]
   print(f'O serial killer {serial_killer["Nome"]} matou {serial_killer["Vítimas"]} vítimas.')

# Salvando os dados atualizados
vitimas_teste_df.to_csv(path_vitimas_teste_previstas, index=True)

print('Vítimas atualizadas com sucesso!')