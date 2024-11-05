from bibliotecas import *
from gerarcsv import gerar_csv
from treino import Treino
from teste import testar_modelo
from conferencia_resultados import conferir_resultados
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from conferencia_resultados import results

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
   
   # Adiciona coluna "Causa Morte" com valor "Desconhecido"
   df["Causa Morte"] = "Desconhecido"
   
   # Salva o arquivo formatado
   df.to_csv("forms.csv", index=False)


@app.get("/gerarcsv")
async def GerarCSV():
      try:
         gerar_csv()
         return{"msg": 200}
      except:
          return{"msg": 400}

@app.get("/treinarModelo")
async def TreinarModelo():
      x=Treino()
      return x

@app.get("/testarModelo")
async def TstModel():
      try: 
         testar_modelo()
         return{"Status": 200}
      except:
         return{"Status": 400}

@app.get("/testarModeloForms")
async def TstModelForms():
      try:
         formatar_forms()
         testar_modelo("forms.csv")
         return{"Status": 200}
      except:
          return{"Status": 400}

@app.get("/conferir")
async def Conferir():
      x= results()
      return{"Resultados": x}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)