from bibliotecas import *

quantidade_vitimas = 2000
vitimas_divisao = quantidade_vitimas / (len(serial_killers) + 8)

def variacao(variacao_min, variacao_max):
   variacao = rd.uniform(variacao_min, variacao_max)
   
   if rd.random() < 0.5:
      variacao *= -1
   
   return variacao
      
def gerar_vitima_preferecial(df, quantidade):
   for killer in serial_killers:
      for i in range(int(quantidade * rd.uniform(0.8, 1.2))):
         vitima = {}
         
         for caracteristica in features_all:
            if caracteristica in caracteristicas_categorias:
               if killer[caracteristica] != 'Todos' and rd.random() < 0.8:
                  vitima[caracteristica] = killer[caracteristica]
               
               else:
                  vitima[caracteristica] = rd.choice(caracteristicas_categorias[caracteristica])
                  
            elif caracteristica in caracteristicas_numericas:
               if rd.random() < 0.8:
                  vitima[caracteristica] = round(killer[caracteristica] + variacao(0, caracteristicas_numericas[caracteristica][3]), 2)
               
               else:
                  vitima[caracteristica] = round(rd.uniform(caracteristicas_numericas[caracteristica][0], caracteristicas_numericas[caracteristica][1]), 2)
            
         vitima['Serial Killer'] = killer['Nome']
         killer['Vítimas'] += 1
         df.append(vitima)

# Função para gerar vítimas aleatórias
def gerar_vitima_aleatoria(df, quantidade):
   for i in range(int(quantidade * rd.uniform(0.8, 1.2))):
      vitima = {}
      
      for caracteristica in features_all:
         if caracteristica in caracteristicas_categorias:
            vitima[caracteristica] = rd.choice(caracteristicas_categorias[caracteristica])
            
         elif caracteristica in caracteristicas_numericas:
            vitima[caracteristica] = round(rd.uniform(caracteristicas_numericas[caracteristica][0], caracteristicas_numericas[caracteristica][1]), 2)
      
      vitima['Serial Killer'] = 'Desconhecido'
      df.append(vitima)

# Gerando vítimas
vitimas_treino = []
gerar_vitima_aleatoria(vitimas_treino, 8 * vitimas_divisao)
gerar_vitima_preferecial(vitimas_treino, vitimas_divisao)
vitimas_treino_df = pd.DataFrame(vitimas_treino)

vitimas_teste = []
gerar_vitima_aleatoria(vitimas_teste, 8 * vitimas_divisao)
gerar_vitima_preferecial(vitimas_teste, vitimas_divisao)
vitimas_teste_resultados_df = pd.DataFrame(vitimas_teste)

# Embaralhando a ordem das vítimas
vitimas_treino_df = vitimas_treino_df.sample(frac=1)
vitimas_teste_resultados_df = vitimas_teste_resultados_df.sample(frac=1)

# Prepara o teste | Remove a coluna 'Serial Killer'
vitimas_teste_df = vitimas_teste_resultados_df.drop('Serial Killer', axis=1)

# Gerando serial killers
serial_killers_df = pd.DataFrame(serial_killers)

# Salvando os dados em arquivos CSV
serial_killers_df.to_csv(path_serial_killers, index=True)
vitimas_treino_df.to_csv(path_vitimas_treino, index=True)
vitimas_teste_df.to_csv(path_vitimas_teste, index=True)
vitimas_teste_resultados_df.to_csv(path_vitimas_teste_resultados, index=True)

print('Arquivos gerados com sucesso!')