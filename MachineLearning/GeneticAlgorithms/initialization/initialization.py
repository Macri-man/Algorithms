import random
import numpy as np
from sklearn.cluster import KMeans

#Random Initialization
def random_initialization(pop_size, chrom_length):
    return [[random.randint(0, 1) for _ in range(chrom_length)] for _ in range(pop_size)]

#Heuristic-Based Initialization
def heuristic_initialization(pop_size, cities):
    # Example: Nearest neighbor heuristic for TSP
    from itertools import permutations
    best_solution = list(range(len(cities)))
    best_distance = float('inf')
    
    for perm in permutations(best_solution):
        distance = sum(cities[perm[i-1]][perm[i]] for i in range(len(perm)))
        if distance < best_distance:
            best_distance = distance
            best_solution = perm
    
    return [list(best_solution) for _ in range(pop_size)]

#Seeded Initialization
def seeded_initialization(pop_size, chrom_length, seeds):
    population = seeds[:]
    while len(population) < pop_size:
        population.append([random.randint(0, 1) for _ in range(chrom_length)])
    return population

#Diverse Initialization
def diverse_initialization(pop_size, chrom_length):
    return (np.random.rand(pop_size, chrom_length) > 0.5).astype(int).tolist()

#Constraint-Based Initialization
def constraint_initialization(pop_size, weight_limit, items):
    population = []
    while len(population) < pop_size:
        individual = [random.randint(0, 1) for _ in range(len(items))]
        if sum(ind * items[i][1] for i, ind in enumerate(individual)) <= weight_limit:
            population.append(individual)
    return population

#Cluster-Based Initialization
def cluster_based_initialization(data, pop_size, chrom_length):
    kmeans = KMeans(n_clusters=pop_size)
    kmeans.fit(data)
    return kmeans.cluster_centers_.astype(int).tolist()

#Gradient-Based Initialization
def gradient_based_initialization(pop_size, gradient_fn, bounds):
    population = []
    for _ in range(pop_size):
        solution = gradient_fn(bounds)
        population.append(solution)
    return population

#Hybrid Initialization
def hybrid_initialization(pop_size, chrom_length, seeds=None):
    population = []
    num_random = pop_size // 2
    num_seeded = pop_size - num_random
    # Random
    for _ in range(num_random):
        population.append([random.randint(0, 1) for _ in range(chrom_length)])
    # Seeded
    if seeds:
        population.extend(seeds[:num_seeded])
    return population

#Opposition-Based Initialization
def opposition_based_initialization(pop_size, chrom_length):
    population = random_initialization(pop_size // 2, chrom_length)
    opposites = [[1 - gene for gene in individual] for individual in population]
    return population + opposites

#Fitness-Proportional Initialization
def fitness_proportional_initialization(pop_size, fitness_fn, bounds):
    population = []
    while len(population) < pop_size:
        candidate = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]
        if random.random() < fitness_fn(candidate):  # Bias by fitness
            population.append(candidate)
    return population

#Incremental Initialization
def incremental_initialization(base_pop_size, increment, total_generations, chrom_length):
    population = []
    for gen in range(total_generations):
        for _ in range(base_pop_size + increment * gen):
            population.append([random.randint(0, 1) for _ in range(chrom_length)])
    return population