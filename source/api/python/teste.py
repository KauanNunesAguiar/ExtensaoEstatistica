from bibliotecas import *

# Carrega dados dos serial killers e das vítimas
serial_killers_df = pd.read_csv(path_serial_killers_previstos)

# Define o limiar mínimo de similaridade para identificar um serial killer
LIMIAR_SIMILARIDADE = 1.1
PESO_NUMERICO = 2.0
PESO_CATEGORICO = 1.4

def calcular_similaridade(vitima, killer, peso_numerico=PESO_NUMERICO, peso_categorico=PESO_CATEGORICO):
    similaridade = 0
    caracteristicas_validas = 0
    
    for caracteristica in features_all:
        # Comparação para características numéricas
        if caracteristica in features_num:
            try:
                diferenca = abs(vitima[caracteristica] - killer[caracteristica])
                max_valor = max(vitima[caracteristica], killer[caracteristica])
                
                if max_valor > 0:  # Evita divisão por zero
                    similaridade += peso_numerico * (1 - diferenca / max_valor)
                    caracteristicas_validas += 1
            except (ValueError, TypeError):
                vitima[caracteristica] = "Desconhecido"

        # Comparação para características categóricas
        elif caracteristica in features_ctg:
            if vitima[caracteristica] not in caracteristicas_categorias[caracteristica]:
                vitima[caracteristica] = "Desconhecido"
            else:
                similaridade += peso_categorico * (vitima[caracteristica] == killer[caracteristica])
                caracteristicas_validas += 1
    
    # Normaliza a similaridade com base no número de características válidas
    if caracteristicas_validas > 0:
        similaridade /= caracteristicas_validas
    
    return similaridade

def identificar_serial_killer(vitima, serial_killers_df, forms = 0):
    melhor_killer = "Desconhecido"
    melhor_similaridade = -1
    
    for _, killer in serial_killers_df.iterrows():
        similaridade = calcular_similaridade(vitima, killer)
        
        if similaridade > melhor_similaridade and (forms != 0 or similaridade >= LIMIAR_SIMILARIDADE):
            melhor_similaridade = similaridade
            melhor_killer = killer['Nome']
    
    return melhor_killer
 
def testar_modelo(path_csv = path_vitimas_teste):
   vitimas_teste_df = pd.read_csv(path_csv)
   if path_csv != path_vitimas_teste:
      vitimas_teste_df['Serial Killer Previsto'] = vitimas_teste_df.apply(lambda x: identificar_serial_killer(x, serial_killers_df, 1), axis=1)
   else:
      vitimas_teste_df['Serial Killer Previsto'] = vitimas_teste_df.apply(lambda x: identificar_serial_killer(x, serial_killers_df), axis=1)
       
   # Salva os resultados em um CSV
   vitimas_teste_df.to_csv(path_csv, index=True)
   print("Modelo testado com sucesso!")
   
if __name__ == "__main__":
   testar_modelo("forms.csv")
