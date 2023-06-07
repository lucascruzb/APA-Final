import random

# Função de aptidão de exemplo
def fitness(individual):
    # Implemente a função de aptidão de acordo com o problema em questão
    # Quanto maior o valor retornado, melhor é o indivíduo
    return sum(individual)

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
gene_length = 10
mutation_rate = 0.1
max_generations = 100

# Gerar população inicial
population = []
for _ in range(population_size):
    individual = [random.randint(0, 9) for _ in range(gene_length)]
    population.append(individual)

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
best_individual = population[fitness_scores.index(max(fitness_scores))]
print("Melhor indivíduo:", best_individual)
print("Aptidão:", fitness(best_individual))
