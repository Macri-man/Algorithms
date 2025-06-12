import numpy as np

def viterbi_algorithm(observations, states, start_probabilities, transition_probabilities, emission_probabilities):
    """
    Implements the Viterbi Algorithm for HMM.

    Parameters:
    - observations: List of observed symbols
    - states: List of hidden states
    - start_probabilities: Array of initial state probabilities
    - transition_probabilities: 2D array of state transition probabilities
    - emission_probabilities: 2D array of observation probabilities

    Returns:
    - best_path: List of most likely states for the observation sequence
    - max_probability: Probability of the best path
    """

    # Number of states
    n_states = len(states)
    n_observations = len(observations)

    # Initialize the Viterbi matrix and path matrix
    viterbi = np.zeros((n_states, n_observations))
    path = np.zeros((n_states, n_observations), dtype=int)

    # Step 1: Initialization
    for i in range(n_states):
        viterbi[i][0] = start_probabilities[i] * emission_probabilities[i][observations[0]]
        path[i][0] = 0  # Starting path for the first observation

    # Step 2: Recursion
    for t in range(1, n_observations):
        for j in range(n_states):
            max_prob = -1
            max_state = -1
            for i in range(n_states):
                prob = viterbi[i][t - 1] * transition_probabilities[i][j] * emission_probabilities[j][observations[t]]
                if prob > max_prob:
                    max_prob = prob
                    max_state = i
            viterbi[j][t] = max_prob
            path[j][t] = max_state

    # Step 3: Termination
    max_prob = -1
    best_last_state = -1
    for i in range(n_states):
        if viterbi[i][n_observations - 1] > max_prob:
            max_prob = viterbi[i][n_observations - 1]
            best_last_state = i

    # Backtrack to find the best path
    best_path = [0] * n_observations
    best_path[-1] = best_last_state
    for t in range(n_observations - 2, -1, -1):
        best_path[t] = path[best_path[t + 1]][t + 1]

    return best_path, max_prob

# Example usage
if __name__ == "__main__":
    # Define parameters
    observations = [0, 1]  # e.g., o_1 = 0, o_2 = 1
    states = [0, 1]  # e.g., S_1 = 0, S_2 = 1
    start_probabilities = np.array([0.6, 0.4])  # π
    transition_probabilities = np.array([[0.7, 0.3],  # A
                                         [0.4, 0.6]])
    emission_probabilities = np.array([[0.5, 0.5],  # B for state 0
                                        [0.1, 0.9]])  # B for state 1

    # Calculate the most likely sequence of states
    best_path, max_probability = viterbi_algorithm(observations, states, start_probabilities, transition_probabilities, emission_probabilities)
    print(f"Best path (states): {best_path}")
    print(f"Probability of the best path: {max_probability:.6f}")
