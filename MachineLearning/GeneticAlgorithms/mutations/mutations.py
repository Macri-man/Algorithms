import random


#Bit Flip
def bit_flip_mutation(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:  # Chance of mutation
            chromosome[i] = 1 - chromosome[i]  # Flip the bit
    return chromosome

#Swap Mutation
def swap_mutation(chromosome, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(chromosome)), 2)  # Select two random indices
        chromosome[i], chromosome[j] = chromosome[j], chromosome[i]  # Swap values
    return chromosome

#Scramble Mutation
def scramble_mutation(chromosome, mutation_rate):
    if random.random() < mutation_rate:
        start, end = sorted(random.sample(range(len(chromosome)), 2))  # Select a range
        scrambled_sublist = chromosome[start:end]
        random.shuffle(scrambled_sublist)  # Shuffle the selected sublist
        chromosome[start:end] = scrambled_sublist  # Place the scrambled sublist back
    return chromosome

#Inversion Mutation
def inversion_mutation(chromosome, mutation_rate):
    if random.random() < mutation_rate:
        start, end = sorted(random.sample(range(len(chromosome)), 2))  # Select a range
        chromosome[start:end] = chromosome[start:end][::-1]  # Reverse the selected range
    return chromosome

#Gaussian Mutation
def gaussian_mutation(chromosome, mutation_rate, sigma=0.1):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] += random.gauss(0, sigma)  # Add Gaussian noise
    return chromosome

#Uniform Mutation
def uniform_mutation(chromosome, mutation_rate, value_range):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = random.uniform(*value_range)  # Assign a random value from the range
    return chromosome

#Non-Uniform Mutation
def non_uniform_mutation(chromosome, mutation_rate, generation, max_generations, value_range):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            delta = (value_range[1] - value_range[0]) * (1 - generation / max_generations)
            chromosome[i] += random.uniform(-delta, delta)  # Apply a shrinking delta over generations
            # Ensure the gene stays within the value range
            chromosome[i] = max(min(chromosome[i], value_range[1]), value_range[0])
    return chromosome

#Boundary Mutation
def boundary_mutation(chromosome, mutation_rate, value_range):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = random.choice([value_range[0], value_range[1]])  # Choose a boundary value
    return chromosome

#Arithmetic Mutation
def arithmetic_mutation(chromosome, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] += chromosome[i] * random.uniform(-0.1, 0.1)  # Adjust by a small percentage
    return chromosome

#Random Resetting
def random_resetting_mutation(chromosome, mutation_rate, value_range):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = random.uniform(*value_range)  # Reset to a random value within the range
    return chromosome