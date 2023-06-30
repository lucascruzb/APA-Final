import random
import numpy as np
from inspyred import ec
from inspyred.ec import terminators

import csv

class TabelaHash:
    def __init__(self):
        self.tabela = {}

    def adicionar_item(self, chave, valor):
        if chave not in self.tabela:
            self.tabela[chave] = [valor]
        else:
            self.tabela[chave].append(valor)

# Função para receber a tabela de produtores de um arquivo CSV
def receber_tabela_produtos():
    produtos = TabelaHash()

    nome_arquivo = "Produtos.csv"

    with open(nome_arquivo, "r", encoding="UTF-8") as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")
        cabecalho = next(leitor)  # Pula a linha do cabeçalho

        for linha in leitor:
            tipo_produto = linha[0]
            produto = linha[1]
            preco = float(linha[2])
            peso = linha[3]
            fornecedor = linha[4]

            item = {
                "Tipo de produto": tipo_produto,
                "Produto": produto,
                "Preço (R$)": preco,
                "Peso": peso,
                "Fornecedor": fornecedor
            }

            produtos.adicionar_item(produto, item)

    return produtos

# Função para receber a tabela de produtos de um arquivo CSV
def receber_tabela_fretes():
    fretes = TabelaHash()

    nome_arquivo = "Fretes.csv"

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")
        cabecalho = next(leitor)  # Pula a linha do cabeçalho
        for linha in leitor:
            fornecedor = linha[0]
            item = {
                "Fornecedor": fornecedor,
                "Frete": float(linha[1])
            }
            fretes.adicionar_item(fornecedor, item)

    return fretes

def receber_tabela_carrinho():
    tabela_produtos = TabelaHash()

    nome_arquivo = "Carrinhos.csv"

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")
        cabecalho = next(leitor)  # Pula a linha do cabeçalho

        for linha in leitor:
            produto = linha[0]
            quantidade = int(linha[1])

            tabela_produtos.adicionar_item(produto, quantidade)

    return tabela_produtos

tabela_carrinho = receber_tabela_carrinho()
tabela_fretes = receber_tabela_fretes()
tabela_produtos = receber_tabela_produtos()

print(tabela_carrinho.tabela)
print(tabela_fretes.tabela)
print(tabela_produtos.tabela)

# def listar_produtores(carrrinho):
#     a = 0;
#     produtores = []
#     for _ in tabela_carrinho.tabela:
#         produtor = individual[a]
#         fornecedor = str(tabela_produtos.tabela[_][produtor]['Fornecedor'])
#         if fornecedor in produtores:
#             pass;
#         else :
#             produtores.append(fornecedor)
#         a +=1;
#     for nome in produtores:
#         if nome is not None: 
#             print(nome)

def fitness(candidates, args):
    
    valorTotal = 0
    produtores = []
    last_15_worst = []  # Armazenar os piores casos dos últimos 15 casos
    for individuo in candidates:
      a = 0
      for _ in tabela_carrinho.tabela:
          produtor = individuo[a]
          valorTotal += tabela_produtos.tabela[_][produtor]['Preço (R$)'] * tabela_carrinho.tabela[_][0]
          fornecedor = str(tabela_produtos.tabela[_][produtor]['Fornecedor'])

          if fornecedor in produtores:
              pass
          else:
              produtores.append(fornecedor)
              valorTotal += tabela_fretes.tabela[fornecedor][0]['Frete']
          a += 1
          if a == len(tabela_carrinho.tabela): 
              
    worst_individual = min(pop)
    last_15_worst.append(worst_individual.fitness)
    
    if len(last_15_worst) > 15:
        last_15_worst.pop(0)  # Remover o caso mais antigo
    
    # Verificar se o pior caso atual é pior que o pior caso dos últimos 15 casos
    if worst_individual.fitness > min(last_15_worst):
        return
    return valorTotal

def generate_random(random, args):
    return [random.randint(0, len(tabela_produtos.tabela[_]) - 1) for _ in tabela_carrinho.tabela]

rand = random.Random()
rand.seed(0)

ea = ec.GA(rand)
ea.selector = ec.selectors.tournament_selection
ea.variator = [ec.variators.uniform_crossover, ec.variators.bit_flip_mutation]
ea.replacer = ec.replacers.generational_replacement
ea.terminator = terminators.generation_termination

max_generations = 100


for generation in range(max_generations):
    pop = ea.evolve(generator=generate_random,
                    evaluator=fitness,
                    pop_size=50,
                    maximize=False)

best_individual = min(pop)
print("Melhor indivíduo:", best_individual.candidate)
print("Fitness:", best_individual.fitness)
