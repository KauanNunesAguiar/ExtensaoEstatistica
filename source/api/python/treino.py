from bibliotecas import *
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar os dados
df_treino = pd.read_csv(path_vitimas_treino)

# Apenas vítimas associadas serão usadas no treinamento
df_treino = df_treino[df_treino['Serial Killer'] != 'Desconhecido']

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
   'Local Morte': [],  # Local onde a vítima foi morta
   'Classe Social': []  # Classe social da vítima
}

def analise_geral(df, graficos):
   print("Análise Geral dos Dados")
   print("=" * 40)
    
   for killer in serial_killers:
      print(f"\nAnalisando o Serial Killer: {killer['Nome']}")
      print("-" * 40)
        
      subset = df[df['Serial Killer'] == killer['Nome']]
      
      serial_killers_dic['Nome'].append(killer['Nome'])
        
      for coluna in features_all:
         # Calcular a média para características numéricas
         if coluna in features_num:
            mediana = round(subset[coluna].median(), 2)
            print(f"\nMediana para {coluna}: {mediana}")
            
            if (graficos):
               plt.figure(figsize=(10, 6))
               sns.kdeplot(subset[coluna], fill=True)
               plt.title(f'Distribuição de {coluna} - {killer["Nome"]}')
               plt.legend([f'Mediana: {mediana}'])
               plt.xlabel(coluna)
               plt.ylabel('Densidade')
               plt.show()
            
            serial_killers_dic[coluna].append(mediana)
         
         # Calcular a distribuição para características categóricas
         elif coluna in features_ctg:
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
               plt.title(f'Distribuição de {coluna} - {killer["Nome"]}')
               plt.legend([f'Mais comum: {subset[coluna].mode()[0]}'])
               plt.xlabel(coluna)
               plt.ylabel('Contagem')
               plt.show()
            
         print("=" * 40)
         
# Função para obter dados de um serial killer específico
def obter_dados_serial_killer(serial_killers_dic, nome):
    dados_serial_killer = {}
    
    # Verifica se o nome está na lista de nomes
    if nome in serial_killers_dic['Nome']:
        indice = serial_killers_dic['Nome'].index(nome)  # Encontra o índice do serial killer
        
        # Itera sobre cada coluna para pegar o dado do índice correspondente
        for coluna, valores in serial_killers_dic.items():
            dados_serial_killer[coluna] = valores[indice]
        
        return dados_serial_killer
    else:
        print(f"Serial killer '{nome}' não encontrado no dicionário.")
        return None
         
# Função para comparar cada categoria de serial_killers_dic com serial_killers para cada serial killer
def comparar_serial_killers():
   for killer in serial_killers:
      
      killer_previsto = obter_dados_serial_killer(serial_killers_dic, killer['Nome'])
      
      print(f"\nComparando Serial Killer: {killer['Nome']} com {killer_previsto['Nome']}")
      print("-" * 40)
      
      for coluna in features_all:
         print(f"\nPrevisão: {killer_previsto[coluna]}")
         print(f"Real: {killer[coluna]}")
         
         if coluna in features_num:
            dif = abs(killer[coluna] - killer_previsto[coluna])
               
            if coluna == 'Altura' and dif < 0.1:
               print(f"{coluna}: Correto")
            elif dif < 5:
               print(f"{coluna}: Correto")
            else:
               print(f"{coluna}: Incorreto")
               
            print(f"Diferença: {round(dif, 2)}")
         
         if coluna in features_ctg:
            if killer[coluna] == killer_previsto[coluna]:
               print(f"{coluna}: Correto")
            else:
               print(f"{coluna}: Incorreto")
         print("=" * 40)

# Função para transformar os dados do DataFrame em um dicionário organizado
def gerar_dicionario_dados_comparacao(df, serial_killers):
    # Apenas vítimas associadas ao serial killer serão usadas
    df = df[df['Serial Killer'] != 'Desconhecido']
    
    # Inicializa o dicionário para armazenar os dados comparativos de cada serial killer
    dados_comparacao = {}
    
    for killer in serial_killers:
        killer_name = killer['Nome']
        subset = df[df['Serial Killer'] == killer_name]
        dados_killer = {'Previsto': {}, 'Esperado': {}}
        
        # Para cada coluna de característica (numérica ou categórica)
        for coluna in features_all:
            # Preenche os valores esperados
            dados_killer['Esperado'][coluna] = killer[coluna]
            
            # Preenche os valores previstos
            if coluna in features_num:
                dados_killer['Previsto'][coluna] = round(subset[coluna].median(), 2)
            elif coluna in features_ctg:
                if subset[coluna].nunique() == 1:
                    dados_killer['Previsto'][coluna] = subset[coluna].mode()[0]
                else:
                    dif = abs(subset[coluna].value_counts().max() - subset[coluna].value_counts().min())
                    dados_killer['Previsto'][coluna] = 'Todos' if dif < subset[coluna].count() / subset[coluna].nunique() else subset[coluna].mode()[0]
        
        # Adiciona o dicionário do serial killer no dicionário principal de comparação
        dados_comparacao[killer_name] = dados_killer
    
    return dados_comparacao

  
def Treino(graficos):
   analise_geral(df_treino, graficos)
   comparar_serial_killers()
   
   serial_killers_df = pd.DataFrame(serial_killers_dic)
   serial_killers_df.to_csv(path_serial_killers_previstos, index=True)
   print('Modelo treinado com sucesso!')
  
def Treino():
    resultado_dicionario = gerar_dicionario_dados_comparacao(df_treino, serial_killers)
    return resultado_dicionario