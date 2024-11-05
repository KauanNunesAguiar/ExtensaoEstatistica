import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# Local dos arquivos
path_serial_killers = 'db/serial_killers.csv'
path_vitimas_treino = 'db/vitimas_treino.csv'
path_vitimas_teste = 'db/vitimas_teste.csv'
path_serial_killers_previstos = 'db/serial_killers_previstos.csv'

features_num = ['Idade', 'Altura', 'Peso']
features_ctg = ['Sexo', 
                  'Cor dos Olhos', 
                  'Cor do Cabelo', 
                  'Causa Morte', 
                  'Local Morte',
                  'Raça', 
                  'Classe Social']
features_all = features_num + features_ctg

caracteristicas_categorias = {
   'Sexo': ['Masculino', 'Feminino'],
   'Cor dos Olhos': ['Azul', 'Verde', 'Castanho', 'Preto'],
   'Cor do Cabelo': ['Loiro', 'Preto', 'Ruivo', 'Castanho'],
   'Causa Morte': ['Esfaqueamento', 'Estrangulamento', 'Envenenamento', 'Contusão'],
   'Local Morte': ['Rua', 'Casa', 'Trabalho', 'Escola'],
   'Raça': ['Branca', 'Parda', 'Negra', 'Amarela'],
   'Classe Social': ['Classe Média', 'Classe Alta', 'Classe Baixa']
}

caracteristicas_numericas = {
   # Nome da característica: [valor mínimo, valor máximo, variação_minima, variação_maxima]
   'Idade': [10, 60, 3, 7],
   'Altura': [1.40, 1.90, 0.07, 0.10],
   'Peso': [30, 90, 3, 7]
}

Elbigodon = {
   'Nome': 'ElBigodon Camacho',
   'Sexo': 'Masculino',
   'Idade': 18,
   'Altura': 1.52,
   'Peso': 40,
   'Cor do Cabelo': 'Loiro',
   'Cor dos Olhos': 'Azul',
   'Raça': 'Branca',
   'Causa Morte': 'Esfaqueamento',
   'Local Morte': 'Rua',
   'Classe Social': 'Classe Média',
   'Vítimas': 0
}

Coringon = {
   'Nome': 'Coringon de le pinheirinho Silva',
   'Sexo': 'Todos',
   'Idade': 40,
   'Altura': 1.68,
   'Peso': 60,
   'Cor do Cabelo': 'Preto',
   'Cor dos Olhos': 'Castanho',
   'Raça': 'Parda',
   'Causa Morte': 'Envenenamento',
   'Local Morte': 'Casa',
   'Classe Social': 'Classe Média',
   'Vítimas': 0
}

Roberto = {
   'Nome': 'Roberto Chimarildo Tomáz',
   'Sexo': 'Feminino',
   'Idade': 26,
   'Altura': 1.80,
   'Peso': 80,
   'Cor do Cabelo': 'Ruivo',
   'Cor dos Olhos': 'Verde',
   'Raça': 'Todos',
   'Causa Morte': 'Estrangulamento',
   'Local Morte': 'Casa',
   'Classe Social': 'Classe Alta',
   'Vítimas': 0
}

serial_killers = [Elbigodon, Coringon, Roberto]



