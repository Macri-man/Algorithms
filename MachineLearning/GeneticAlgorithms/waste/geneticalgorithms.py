import random

# Parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.01
GENERATIONS = 100
GENOME_LENGTH = 10  # Binary representation length

# Fitness function
def fitness_function(individual):
    # Convert binary string to integer
    x = int(individual, 2)
    return x ** 2  # Example function: f(x) = x^2

# Create initial population
def create_population(size):
    return [''.join(random.choice('01') for _ in range(GENOME_LENGTH)) for _ in range(size)]

# Selection using tournament selection
def select(population):
    tournament_size = 5
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=fitness_function)

# Crossover two individuals
def crossover(parent1, parent2):
    crossover_point = random.randint(1, GENOME_LENGTH - 1)
    return parent1[:crossover_point] + parent2[crossover_point:]

# Mutation of an individual
def mutate(individual):
    return ''.join(gene if random.random() > MUTATION_RATE else random.choice('01') for gene in individual)

# Genetic Algorithm
def genetic_algorithm():
    population = create_population(POPULATION_SIZE)
    
    for generation in range(GENERATIONS):
        # Evaluate fitness
        population = sorted(population, key=fitness_function, reverse=True)

        # Print best individual and its fitness
        print(f"Generation {generation}: Best = {population[0]}, Fitness = {fitness_function(population[0])}")

        # Create next generation
        new_population = []
        for _ in range(POPULATION_SIZE):
            parent1 = select(population)
            parent2 = select(population)
            offspring = crossover(parent1, parent2)
            new_population.append(mutate(offspring))
        
        population = new_population

# Run the genetic algorithm
if __name__ == "__main__":
    genetic_algorithm()
