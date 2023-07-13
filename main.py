import random

import csv

class TabelaHash:
    def __init__(self):
        self.tabela = {}

    def adicionar_item(self, chave, valor):
        if chave not in self.tabela:
            self.tabela[chave] = valor
        else:
            if not isinstance(self.tabela[chave], list):
                self.tabela[chave] = [self.tabela[chave]]
            self.tabela[chave].append(valor)
        

    def adicionar_score(self, chave, score):
        self.tabela[chave].append(score)

# Função de seleção para o cruzamento (elitista)
def selection_elitist(population, fitness_scores, num_parents):
    # Selecionar os melhores indivíduos (menor aptidão) como pais
    sorted_population = sorted(zip(fitness_scores, population), key=lambda x: x[0])
    selected_parents = [x[1] for x in sorted_population[:int(num_parents)]]
    return selected_parents

def listar_produtores():
    a = 0;
    produtores = []
    for _ in tabela_carrinho.tabela:
        produtor = individual[a]
        fornecedor = str(tabela_produtos.tabela[_][produtor]['Fornecedor'])
        if fornecedor in produtores:
            pass;
        else :
            produtores.append(fornecedor)
        a +=1;
    for nome in produtores:
        if nome is not None: 
            print(nome)

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

# Função para receber a tabela de produtos de um arquivo CSV
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
# print(tabela_carrinho.tabela)
# print(tabela_fretes.tabela)
# print(tabela_produtos.tabela)

# Função de aptidão de exemplo
def fitness(individual):
    a = 0;
    valorTotal =0;
    produtores = []
    for _ in tabela_carrinho.tabela:
        produtor = individual[a]
        valorTotal += tabela_produtos.tabela[_][produtor]['Preço (R$)'] * tabela_carrinho.tabela[_]
        fornecedor = str(tabela_produtos.tabela[_][produtor]['Fornecedor'])
        if fornecedor in produtores:
            pass;
        else :
            produtores.append(fornecedor)
            valorTotal += tabela_fretes.tabela[fornecedor]['Frete']
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
    return Population(mutated_individual, fitness(mutated_individual))

# Parâmetros do algoritmo genético
population_size = 100000
gene_length = len(tabela_carrinho.tabela)
mutation_rate = 0.5
max_generations = 1000
num_parents = population_size/4000

class Population:
    def __init__(self, individuo, score):
        self.individuo = individuo
        self.score = score
# Gerar população inicial
population = []
for i in range(population_size):
    individual = []
    for _ in tabela_carrinho.tabela:
        individual.append(random.randint(0, len(tabela_produtos.tabela[_]) - 1))
    population.append(Population(individual, fitness(individual)))

# Executar o algoritmo genético
stop = 0
generation = 0
while generation < max_generations:
    # Avaliar aptidão
    fitness_scores = [objeto.score for objeto in population]

    # Seleção
    selected_parents = selection_elitist(population, fitness_scores, num_parents)

    # Cruzamento
    new_population = []
    for i in range(int(population_size/2)):
        parent1 = random.choice(selected_parents)
        parent2 = random.choice(selected_parents)
        child1, child2 = crossover(parent1.individuo, parent2.individuo)
        new_population.append(Population(child1, fitness(child1)))
        new_population.append(Population(child2,fitness(child2)))

    # Mutação
    mutated_population = [mutate(individual.individuo, mutation_rate) for individual in new_population]


    # Avaliar aptidão dos novos indivíduos
    fitness_scores_mutated = [objeto.score for objeto in mutated_population]

    # Substituir apenas os indivíduos com fitness_score maior do que os novos indivíduos

    if min(fitness_scores) <= min(fitness_scores_mutated):
        stop +=1
        if stop == 50:
            break
    else : 
        stop = 0

    # Selecionar os 10 melhores indivíduos da população atual
    sorted_population = sorted(population, key=lambda x: x.score)
    top_individuals = sorted_population[:10]
    

    # Substituir os demais indivíduos pelos seus filhos correspondentes
    new_population = top_individuals + mutated_population[len(top_individuals):]

    # Atualizar a população
    population = new_population
    fitness_scores = [objeto.score for objeto in population]

    # Imprimir o melhor indivíduo da geração atual
    best_individual = population[fitness_scores.index(min(fitness_scores))]
    print(f"Geração {generation + 1} - Melhor indivíduo (população): {best_individual.individuo} - Aptidão: {fitness(best_individual.individuo)}")

    generation += 1

best_individual = population[fitness_scores.index(min(fitness_scores))]
print("Melhor indivíduo:", best_individual.individuo)
print("Produtores:")
listar_produtores()
print("Aptidão:", fitness(best_individual.individuo))
