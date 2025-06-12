import numpy as np

def forward_algorithm(observations, states, start_probabilities, transition_probabilities, emission_probabilities):
    """
    Implements the Forward Algorithm for HMM.

    Parameters:
    - observations: List of observed symbols
    - states: List of hidden states
    - start_probabilities: Array of initial state probabilities
    - transition_probabilities: 2D array of state transition probabilities
    - emission_probabilities: 2D array of observation probabilities

    Returns:
    - total_probability: Probability of the observation sequence
    """

    # Number of states
    n_states = len(states)
    n_observations = len(observations)

    # Initialize the forward matrix
    alpha = np.zeros((n_states, n_observations))

    # Step 1: Initialization
    for i in range(n_states):
        alpha[i][0] = start_probabilities[i] * emission_probabilities[i][observations[0]]

    # Step 2: Induction
    for t in range(1, n_observations):
        for j in range(n_states):
            alpha[j][t] = sum(alpha[i][t-1] * transition_probabilities[i][j] for i in range(n_states)) * emission_probabilities[j][observations[t]]

    # Step 3: Termination
    total_probability = sum(alpha[i][n_observations - 1] for i in range(n_states))

    return total_probability

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

    # Calculate the probability of the observation sequence
    probability = forward_algorithm(observations, states, start_probabilities, transition_probabilities, emission_probabilities)
    print(f"Probability of the observation sequence: {probability:.6f}")
