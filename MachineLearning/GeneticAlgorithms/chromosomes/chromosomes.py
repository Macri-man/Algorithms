import random

#Binary Chromosomes
def create_binary_chromosome(length):
    return [random.choice([0, 1]) for _ in range(length)]

#Integer Chromosomes
def create_integer_chromosome(length, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(length)]

#Floating-Point Chromosomes
def create_float_chromosome(length, min_val, max_val):
    return [random.uniform(min_val, max_val) for _ in range(length)]

#Permutation Chromosomes
def create_permutation_chromosome(elements):
    chromosome = elements[:]
    random.shuffle(chromosome)
    return chromosome

#Tree Chromosomes
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def create_tree_chromosome(depth, operators, operands):
    if depth == 0:
        return TreeNode(random.choice(operands))
    operator = random.choice(operators)
    left = create_tree_chromosome(depth - 1, operators, operands)
    right = create_tree_chromosome(depth - 1, operators, operands)
    return TreeNode(operator, left, right)

#Vector Chromosomes
def create_vector_chromosome(length):
    return [random.random() for _ in range(length)]

#Graph-Based Chromosomes
# Create a graph as an adjacency list
def create_graph_chromosome(num_nodes, num_edges):
    graph = {node: [] for node in range(num_nodes)}
    edges = set()

    while len(edges) < num_edges:
        u, v = random.sample(range(num_nodes), 2)
        # Avoid duplicate edges and self-loops
        if u != v and (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
            graph[u].append(v)
            graph[v].append(u)
    
    return graph