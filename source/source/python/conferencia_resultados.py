from bibliotecas import *
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# Calcula False Positives, False Negatives, True Positives e True Negatives
def calcular_resultados(df_resultados):
   fp = 0
   fn = 0
   tp = 0
   tn = 0
   erros = 0
   
   for i in range(len(df_resultados)):
      if df_resultados['Real'][i] == 'Desconhecido' and df_resultados['Previsto'][i] == 'Desconhecido':
         tn += 1
      
      elif df_resultados['Real'][i] == 'Desconhecido' and df_resultados['Previsto'][i] != 'Desconhecido':
         fn += 1
      
      elif df_resultados['Real'][i] != 'Desconhecido' and df_resultados['Previsto'][i] == 'Desconhecido':
         fp += 1
      
      elif df_resultados['Real'][i] != 'Desconhecido' and df_resultados['Previsto'][i] != 'Desconhecido':
         if df_resultados['Real'][i] == df_resultados['Previsto'][i]:
            tp += 1
         else:
            fp += 1
   
   return tp, tn, fp, fn

# Mostra os resultados
def mostrar_resultados(tp, tn, fp, fn):
   
   # Criação dos arrays de verdade e predição
   y_true = [1] * tp + [0] * tn + [1] * fn + [0] * fp
   y_pred = [1] * tp + [0] * tn + [0] * fn + [1] * fp

   precisao = precision_score(y_true, y_pred)
   recall = recall_score(y_true, y_pred)
   f1 = f1_score(y_true, y_pred)
   acuracia = accuracy_score(y_true, y_pred)
   matriz_confusao = confusion_matrix(y_true, y_pred)
   
   # Ajusta as variáveis para porcentagem
   precisao = round(precisao * 100, 2)
   recall = round(recall * 100, 2)
   f1 = round(f1 * 100, 2)
   acuracia = round(acuracia * 100, 2)
   
   print("False Positives: ", fp)
   print("False Negatives: ", fn)
   print("True Positives: ", tp)
   print("True Negatives: ", tn)
   print("=" * 40)
   print(f"Acurácia: {acuracia}%")
   print(f"Precisão: {precisao}%")
   print(f"Recall: {recall}%")
   print(f"F1 Score: {f1}%")
   print(f"Matriz de Confusão: \n{matriz_confusao}")
   return acuracia, precisao, recall, f1

def conferir_resultados():
   df_resultados = prepara_resultados()
   
   # Calcula os resultados
   tp, tn, fp, fn = calcular_resultados(df_resultados)
   acuracia, precisao, recall, f1 = mostrar_resultados(tp, tn, fp, fn)
   
   # Salva tp, tn, fp, fn, erros, acuracia, precisao, recall e f1 em um arquivo CSV
   resultados = {
      'True Positives': [tp],
      'True Negatives': [tn],
      'False Positives': [fp],
      'False Negatives': [fn],
      'Acuracia': [acuracia],
      'Precisao': [precisao],
      'Recall': [recall],
      'F1 Score': [f1]
   }
   
   df_resultados = pd.DataFrame(resultados)
   df_resultados.to_csv('db/resultados.csv', index=False)
   print("Resultados salvos com sucesso!")
   
def prepara_resultados():
   # Carrega os dados
   df_teste = pd.read_csv(path_vitimas_teste)
   
   # Cria um único dataframe somente com as colunas 'Serial Killer Real' e 'Serial Killer Previsto'
   df_resultados = df_teste[['Serial Killer Real', 'Serial Killer Previsto']]
   
   # Renomeia as colunas
   df_resultados.columns = ['Real', 'Previsto']
   
   return df_resultados
   
if __name__ == "__main__":
   conferir_resultados()