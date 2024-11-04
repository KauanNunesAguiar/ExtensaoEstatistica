from bibliotecas import *

# Carrega dados dos serial killers e das vítimas
serial_killers_df = pd.read_csv(path_serial_killers)
vitimas_teste_df = pd.read_csv(path_vitimas_teste)

# Lista de características que iremos considerar para o matching

def calcular_similaridade(vitima, killer, peso_numerico=1.0, peso_categorico=1.0):
    """
    Calcula a similaridade entre uma vítima e um serial killer com base nas características.
    """
    similaridade = 0
    
    for caracteristica in features_all:
        # Comparação para características numéricas
        if caracteristica in features_num:
            similaridade += peso_numerico * (1 - abs(vitima[caracteristica] - killer[caracteristica]) / max(vitima[caracteristica], killer[caracteristica]))
        
        # Comparação para características categóricas
        elif caracteristica in features_ctg:
            similaridade += peso_categorico * (vitima[caracteristica] == killer[caracteristica])
    
    return similaridade

def identificar_serial_killer(vitima, serial_killers_df):
    """
    Identifica o serial killer mais provável para uma vítima.
    """
    melhor_killer = None
    melhor_similaridade = -1
    
    for _, killer in serial_killers_df.iterrows():
        similaridade = calcular_similaridade(vitima, killer)
        
        if similaridade > melhor_similaridade:
            melhor_similaridade = similaridade
            melhor_killer = killer['Nome']
    
    return melhor_killer

# Realiza a identificação para cada vítima em vitimas_teste_df
vitimas_teste_df['Serial Killer'] = vitimas_teste_df.apply(lambda x: identificar_serial_killer(x, serial_killers_df), axis=1)

# Salva os resultados em um CSV
vitimas_teste_df.to_csv(path_vitimas_teste_previstas, index=True)
print("Arquivo com serial killers estimados gerado com sucesso!")
