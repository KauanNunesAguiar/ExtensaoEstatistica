from bibliotecas import *
from gerarcsv import gerar_csv
from treino import treinar_modelo
from teste import testar_modelo
from conferencia_resultados import conferir_resultados

def formatar_forms():
   df = pd.read_csv("forms.csv")
   
   if "Carimbo de data/hora" in df.columns:
      df = df.drop(columns=["Carimbo de data/hora"])
      
   df = df.rename(columns={"Qual seu nome?": "Nome",  
                           "Qual seu sexo biologico?": "Sexo",          
                           "Qual a sua idade?": "Idade",  
                           "Qual a sua altura em metros? (exemplo: 1.72)": "Altura",      
                           "Qual o seu peso em kg? (exemplo 63.2)": "Peso",        
                           "Qual a cor de seu cabelo?": "Cor do Cabelo",
                           "Qual a cor de seus olhos?": "Cor dos Olhos",
                           "Qual sua raça?": "Raça",
                           "Entre as seguintes opções, onde você passa a maior parte do dia?": "Local Morte",
                           "Qual sua classe social?": "Classe Social"})
   
   # Adiciona colunas faltantes com valor "Desconhecido"
   for coluna in features_all:
      if coluna not in df.columns:
         df[coluna] = "Desconhecido"
   
   # Salva o arquivo formatado
   df.to_csv("forms.csv", index=False)

if __name__ == "__main__":
   while True:
      print("Menu:")
      print("1 - Gerar CSV")
      print("2 - Treinar Modelo (com gráficos)")
      print("3 - Treinar Modelo (sem gráficos)")
      print("4 - Testar Modelo")
      print("5 - Testar Modelo (forms.csv)")
      print("6 - Conferir Resultados")
      print("7 - Sair")
      
      opcao = input("Escolha uma opção: ")
      
      if opcao == "1":
         gerar_csv()
      elif opcao == "2":
         treinar_modelo(True)
      elif opcao == "3":
         treinar_modelo(False)
      elif opcao == "4":
         testar_modelo()
      elif opcao == "5":
         formatar_forms()
         testar_modelo("forms.csv")
      elif opcao == "6":
         conferir_resultados()
      elif opcao == "7":
         break
      else:
         print("Opção inválida!")
      print("=" * 40)
      