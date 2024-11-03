import pandas as pd
import random

# Local onde o arquivo será salvo
path_serial_killers = 'serial_killers.csv'
path_vitimas_treino = 'vitimas_treino.csv'
path_vitimas_teste = 'vitimas_teste.csv'

quantidade_vitimas = 100000

# Dados dos serial killers
serial_killers = {
   'Nome': ['ElBigodon Camacho', 'Coringon de le pinheirinho Silva', 'Roberto Chimarildo Tomáz'],
   'Sexo': ['Todos', 'Todos', 'Feminino'],
   'Idade': [18, 40, 26],
   'Altura': [1.52, 1.68, 1.80],
   'Peso': [40, 60, 80],
   'Cor do Cabelo': ['Loiro', 'Preto', 'Ruivo'],
   'Cor dos Olhos': ['Azul', 'Castanho', 'Verde'],
   'Raça': ['Branca', 'Parda', 'Todos'],
   'Causa Morte': ['Esfaqueamento', 'Envenenamento', 'Estrangulamento'],  # Método de assassinato
   'Local': ['Rua', 'Casa', 'Casa'],  # Local onde a vítima foi morta
   'Classe Social': ['Classe Média', 'Classe Média', 'Classe Alta'],
   'Vítimas': [0, 0, 0]
}

serial_killers_df = pd.DataFrame(serial_killers)

# Função para gerar vítimas aleatórias
def gerar_vitima():
   sexo = random.choice(['Masculino', 'Feminino'])  # Sexo da vítima
   idade = random.randint(10, 60)  # Idades entre 18 e 50
   altura = round(random.uniform(1.40, 1.90), 2)  # Altura entre 1.50 e 1.90
   peso = random.randint(30, 90)  # Peso entre 30 e 90
   cor_dos_olhos = random.choice(['Azul', 'Castanho', 'Verde'])  # Cor dos olhos
   cor_do_cabelo = random.choice(['Loiro', 'Preto', 'Ruivo'])  # Cor do cabelo
   raça = random.choice(['Branca', 'Parda', 'Negra']) # Raça da vítima
   causa_morte = random.choice(['Esfaqueamento', 'Envenenamento', 'Estrangulamento', 'Esfaqueamento', 'Envenenamento', 'Estrangulamento', 'Contusão'])  # Método de assassinato
   local = random.choice(['Rua', 'Rua', 'Casa', 'Casa', 'Trabalho'])  # Local onde a vítima foi morta
   classe_social = random.choice(['Classe Média', 'Classe Média', 'Classe Alta', 'Classe Alta', 'Classe Baixa'])  # Classe social da vítima
   
   return {'Sexo': sexo, 'Idade': idade, 'Altura': altura, 'Peso': peso, 'Cor dos Olhos': cor_dos_olhos, 'Cor do Cabelo': cor_do_cabelo, 'Causa Morte': causa_morte, 'Local': local, 'Raça': raça, 'Classe Social': classe_social}

# Gerando vítimas
vitimas_treino = [gerar_vitima() for id in range(quantidade_vitimas)]
vitimas_treino_df = pd.DataFrame(vitimas_treino)

vitimas_teste = [gerar_vitima() for id in range(quantidade_vitimas)]
vitimas_teste_df = pd.DataFrame(vitimas_teste)

# Salvando os dados em arquivos CSV
serial_killers_df.to_csv(path_serial_killers, index=True)
vitimas_treino_df.to_csv(path_vitimas_treino, index=True)
vitimas_teste_df.to_csv(path_vitimas_teste, index=True)

print('Arquivos gerados com sucesso!')
