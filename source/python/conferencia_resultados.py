from bibliotecas import *

# Carregar os dados
df_teste_previstas = pd.read_csv(path_vitimas_teste_previstas)
df_teste_resultados = pd.read_csv(path_vitimas_teste_resultados)

# Organiza por index
df_teste_previstas = df_teste_previstas.sort_index()
df_teste_resultados = df_teste_resultados.sort_index()

# Calcula False Positives, False Negatives, True Positives e True Negatives
def calcular_resultados(df_previstas, df_resultados):
   fp = 0
   fn = 0
   tp = 0
   tn = 0
   
   for i in range(len(df_previstas)):
      if df_previstas['Serial Killer'][i] == 'Desconhecido' and df_resultados['Serial Killer'][i] == 'Desconhecido':
         tn += 1
      
      elif df_previstas['Serial Killer'][i] == 'Desconhecido' and df_resultados['Serial Killer'][i] != 'Desconhecido':
         fp += 1
      
      elif df_previstas['Serial Killer'][i] != 'Desconhecido' and df_resultados['Serial Killer'][i] == 'Desconhecido':
         fn += 1
      
      elif df_previstas['Serial Killer'][i] != 'Desconhecido' and df_resultados['Serial Killer'][i] != 'Desconhecido':
         if df_previstas['Serial Killer'][i] == df_resultados['Serial Killer'][i]:
            tp += 1
          
         else:
            fp += 1
            fn += 1
   
   return tp, tn, fp, fn

# Calcula a acurácia
def calcular_acuracia(tp, tn, fp, fn):
   return (tp + tn) / (tp + tn + fp + fn)

# Calcula a precisão
def calcular_precisao(tp, fp):
   return tp / (tp + fp)

# Calcula o recall
def calcular_recall(tp, fn):
   return tp / (tp + fn)

# Calcula o F1 Score
def calcular_f1_score(precisao, recall):
   return 2 * (precisao * recall) / (precisao + recall)

# Calcula a matriz de confusão
def calcular_matriz_confusao(tp, tn, fp, fn):
   return [[tp, fp], [fn, tn]]

# Mostra os resultados
def mostrar_resultados(tp, tn, fp, fn):
   acuracia = round(calcular_acuracia(tp, tn, fp, fn) * 100, 2)
   precisao = round(calcular_precisao(tp, fp) * 100, 2)
   recall = round(calcular_recall(tp, fn) * 100, 2)
   f1_score = round(calcular_f1_score(precisao, recall) * 100, 2)
   matriz_confusao = calcular_matriz_confusao(tp, tn, fp, fn)
   
   print("False Positives: ", fp)
   print("False Negatives: ", fn)
   print("True Positives: ", tp)
   print("True Negatives: ", tn)
   print("=" * 40)
   print(f"Acurácia: {acuracia}%")
   print(f"Precisão: {precisao}%")
   print(f"Recall: {recall}%")
   print(f"F1 Score: {f1_score}%")
   print(f"Matriz de Confusão: {matriz_confusao}")
   return

# Calcula os resultados
tp, tn, fp, fn = calcular_resultados(df_teste_previstas, df_teste_resultados)
mostrar_resultados(tp, tn, fp, fn)

