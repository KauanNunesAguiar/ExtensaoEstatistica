from bibliotecas import *
from gerarcsv import gerar_csv
from treino import treinar_modelo
from teste import testar_modelo
from conferencia_resultados import conferir_resultados

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
         testar_modelo("forms.csv")
      elif opcao == "6":
         conferir_resultados()
      elif opcao == "7":
         break
      else:
         print("Opção inválida!")
      print("=" * 40)
      