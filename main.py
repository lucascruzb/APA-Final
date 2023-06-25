import random

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

# Exemplo de uso

tabela_carrinho = receber_tabela_carrinho()
tabela_fretes = receber_tabela_fretes()
tabela_produtos = receber_tabela_produtos()

# Acesso às informações da tabela hash
print(tabela_carrinho.tabela)
print(tabela_fretes.tabela)
print(tabela_produtos.tabela)

# Função de aptidão de exemplo
def fitness(individual):
    a = 0;
    valorTotal =0;
    produtores = []
    for _ in tabela_carrinho.tabela:
        produtor = individual[a]
        valorTotal += tabela_produtos.tabela[_][produtor]['Preço (R$)'] * tabela_carrinho.tabela[_][0]
        fornecedor = str(tabela_produtos.tabela[_][produtor]['Fornecedor'])
        if fornecedor in produtores:
            pass;
        else :
            produtores.append(fornecedor)
            valorTotal += tabela_fretes.tabela[fornecedor][0]['Frete']
        a +=1;

    return valorTotal

# Função de cruzamento (crossover)
def crossover(parent1, parent2):
    # Implemente o crossover de acordo com a estratégia desejada
    # Neste exemplo, é realizado um ponto de corte único
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Função de mutação
def mutate(individual, mutation_rate):
    # Implemente a mutação de acordo com a estratégia desejada
    # Neste exemplo, cada gene do indivíduo tem uma chance de ser mutado
    mutated_individual = []
    for gene in individual:
        if random.random() < mutation_rate:
            mutated_individual.append(random.randint(0, 9))
        else:
            mutated_individual.append(gene)
    return mutated_individual

# Parâmetros do algoritmo genético
population_size = 100
gene_length = len(tabela_carrinho.tabela)
mutation_rate = 0.1
max_generations = 100

# Gerar população inicial
population = []
for i in range(100):
    individual = []
    for _ in tabela_carrinho.tabela:
        individual.append(random.randint(0, len(tabela_produtos.tabela[_])-1))
    population.append(individual)
    individual.clear

# Executar o algoritmo genético
for generation in range(max_generations):
    # Avaliar aptidão
    fitness_scores = [fitness(individual) for individual in population]

    # Verificar critério de parada
    if max(fitness_scores) == gene_length:
        break

    # Seleção
    selected_parents = random.choices(population, weights=fitness_scores, k=population_size)

    # Cruzamento
    new_population = []
    for i in range(0, population_size, 2):
        parent1 = selected_parents[i]
        parent2 = selected_parents[i + 1]
        child1, child2 = crossover(parent1, parent2)
        new_population.extend([child1, child2])

    # Mutação
    mutated_population = [mutate(individual, mutation_rate) for individual in new_population]

    # Atualizar população
    population = mutated_population

# Imprimir resultado
best_individual = population[fitness_scores.index(min(fitness_scores))]
print("Melhor indivíduo:", best_individual)
print("Aptidão:", fitness(best_individual))
