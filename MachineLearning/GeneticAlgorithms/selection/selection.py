import random
import math

#Roulette Wheel Selection
def roulette_wheel_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    probabilities = [f / total_fitness for f in fitness_values]
    cumulative_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
    
    rand = random.random()
    for i, cumulative in enumerate(cumulative_probabilities):
        if rand <= cumulative:
            return population[i]
        
#Rank-Based Selection
def rank_based_selection(population, fitness_values):
    sorted_population = [x for _, x in sorted(zip(fitness_values, population))]
    ranks = range(1, len(population) + 1)
    total_rank = sum(ranks)
    probabilities = [rank / total_rank for rank in ranks]
    cumulative_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
    
    rand = random.random()
    for i, cumulative in enumerate(cumulative_probabilities):
        if rand <= cumulative:
            return sorted_population[i]
        
#Tournament Selection
def tournament_selection(population, fitness_values, tournament_size=3):
    participants = random.sample(list(zip(population, fitness_values)), tournament_size)
    winner = max(participants, key=lambda x: x[1])
    return winner[0]


#Truncation Selection
def truncation_selection(population, fitness_values, proportion=0.5):
    sorted_population = [x for _, x in sorted(zip(fitness_values, population), reverse=True)]
    cutoff = int(len(population) * proportion)
    return random.choice(sorted_population[:cutoff])


#Stochastic Universal Sampling (SUS)
def stochastic_universal_sampling(population, fitness_values, num_selected):
    total_fitness = sum(fitness_values)
    point_distance = total_fitness / num_selected
    start_point = random.uniform(0, point_distance)
    points = [start_point + i * point_distance for i in range(num_selected)]
    
    selected = []
    cumulative_fitness = 0
    index = 0
    for point in points:
        while cumulative_fitness < point:
            cumulative_fitness += fitness_values[index]
            index += 1
        selected.append(population[index - 1])
    return selected

#Boltzmann Selection
def boltzmann_selection(population, fitness_values, temperature):
    adjusted_fitness = [math.exp(f / temperature) for f in fitness_values]
    total_fitness = sum(adjusted_fitness)
    probabilities = [f / total_fitness for f in adjusted_fitness]
    cumulative_probabilities = [sum(probabilities[:i+1]) for i in range(len(probabilities))]
    
    rand = random.random()
    for i, cumulative in enumerate(cumulative_probabilities):
        if rand <= cumulative:
            return population[i]
        
#Elitism
def elitism_selection(population, fitness_values, num_elites=1):
    elite_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i], reverse=True)[:num_elites]
    return [population[i] for i in elite_indices]

#Random Selection
def random_selection(population):
    return random.choice(population)

#Fitness Sharing (for diversity)
def fitness_sharing(fitness_values, population, sharing_distance=1.0):
    shared_fitness = []
    for i, indiv in enumerate(population):
        sharing_sum = 0
        for j, other_indiv in enumerate(population):
            distance = abs(indiv - other_indiv)  # Assuming numerical representation
            if distance < sharing_distance:
                sharing_sum += 1 - (distance / sharing_distance)
        shared_fitness.append(fitness_values[i] / sharing_sum)
    return shared_fitness