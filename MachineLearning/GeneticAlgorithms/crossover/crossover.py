import random

#Single-Point Crossover
def single_point_crossover(parent1, parent2):
    # Ensure both parents are the same length
    assert len(parent1) == len(parent2), "Parents must be of the same length"
    
    # Choose a random crossover point
    point = random.randint(1, len(parent1) - 1)
    
    # Create offspring by swapping genes after the crossover point
    offspring1 = parent1[:point] + parent2[point:]
    offspring2 = parent2[:point] + parent1[point:]
    
    return offspring1, offspring2

#Two-Point Crossover
def two_point_crossover(parent1, parent2):
    # Ensure both parents are the same length
    assert len(parent1) == len(parent2), "Parents must be of the same length"
    
    # Choose two random crossover points
    point1 = random.randint(1, len(parent1) - 2)
    point2 = random.randint(point1 + 1, len(parent1) - 1)
    
    # Create offspring by swapping genes between the points
    offspring1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    offspring2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    
    return offspring1, offspring2

#Uniform Crossover
def uniform_crossover(parent1, parent2):
    # Ensure both parents are the same length
    assert len(parent1) == len(parent2), "Parents must be of the same length"
    
    offspring1, offspring2 = [], []
    
    for gene1, gene2 in zip(parent1, parent2):
        # Randomly choose which parent's gene to inherit for each position
        if random.random() < 0.5:
            offspring1.append(gene1)
            offspring2.append(gene2)
        else:
            offspring1.append(gene2)
            offspring2.append(gene1)
    
    return offspring1, offspring2

#Arithmetic Crossover
def arithmetic_crossover(parent1, parent2, alpha=0.5):
    # Ensure both parents are the same length
    assert len(parent1) == len(parent2), "Parents must be of the same length"
    
    # Create offspring using a weighted average
    offspring1 = [alpha * g1 + (1 - alpha) * g2 for g1, g2 in zip(parent1, parent2)]
    offspring2 = [(1 - alpha) * g1 + alpha * g2 for g1, g2 in zip(parent1, parent2)]
    
    return offspring1, offspring2

#Blend Crossover (BLX-α)
def blend_crossover(parent1, parent2, alpha=0.5):
    # Ensure both parents are the same length
    assert len(parent1) == len(parent2), "Parents must be of the same length"
    
    offspring1, offspring2 = [], []
    
    for g1, g2 in zip(parent1, parent2):
        # Create offspring by blending genes within a range defined by alpha
        lower = min(g1, g2) - alpha * abs(g1 - g2)
        upper = max(g1, g2) + alpha * abs(g1 - g2)
        offspring1.append(random.uniform(lower, upper))
        offspring2.append(random.uniform(lower, upper))
    
    return offspring1, offspring2

#Partially Matched Crossover (PMX)
def partially_matched_crossover(parent1, parent2):
    # Ensure both parents are the same length
    assert len(parent1) == len(parent2), "Parents must be of the same length"
    
    size = len(parent1)
    point1 = random.randint(0, size - 2)
    point2 = random.randint(point1 + 1, size - 1)
    
    offspring1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    offspring2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    
    # Repair the offspring to maintain uniqueness in the permutation
    offspring1 = repair_pmx(offspring1, parent1, parent2, point1, point2)
    offspring2 = repair_pmx(offspring2, parent2, parent1, point1, point2)
    
    return offspring1, offspring2

def repair_pmx(offspring, parent1, parent2, point1, point2):
    for i in range(point1, point2):
        if offspring[i] in offspring[:point1] + offspring[point2:]:
            # Repair by replacing duplicate genes with the missing ones
            missing_gene = set(parent1 + parent2) - set(offspring)
            offspring[i] = missing_gene.pop()
    return offspring

#Order Crossover (OX)
def order_crossover(parent1, parent2):
    # Ensure both parents are the same length
    assert len(parent1) == len(parent2), "Parents must be of the same length"
    
    size = len(parent1)
    point1 = random.randint(0, size - 2)
    point2 = random.randint(point1 + 1, size - 1)
    
    # Copy the section between points from parent1 to offspring1
    offspring1 = [-1] * size
    offspring1[point1:point2] = parent1[point1:point2]
    
    # Copy the remaining genes from parent2
    current_index = point2
    for gene in parent2:
        if gene not in offspring1:
            if current_index == size:
                current_index = 0
            offspring1[current_index] = gene
            current_index += 1
    
    # Repeat for offspring2
    offspring2 = [-1] * size
    offspring2[point1:point2] = parent2[point1:point2]
    current_index = point2
    for gene in parent1:
        if gene not in offspring2:
            if current_index == size:
                current_index = 0
            offspring2[current_index] = gene
            current_index += 1
    
    return offspring1, offspring2

#Cycle Crossover (CX)
def cycle_crossover(parent1, parent2):
    # Ensure both parents are the same length
    assert len(parent1) == len(parent2), "Parents must be of the same length"
    
    size = len(parent1)
    offspring1 = [-1] * size
    offspring2 = [-1] * size
    
    # Start with the first unfilled position in offspring1
    i = 0
    while -1 in offspring1:
        # Traverse cycles
        current = i
        while offspring1[current] == -1:
            offspring1[current] = parent1[current]
            offspring2[current] = parent2[current]
            current = parent2.index(parent1[current])
    
    return offspring1, offspring2