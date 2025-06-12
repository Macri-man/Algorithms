import numpy as np

def forward_algorithm(observations, states, start_probabilities, transition_probabilities, emission_probabilities):
    n_states = len(states)
    n_observations = len(observations)
    alpha = np.zeros((n_states, n_observations))

    # Initialization
    for i in range(n_states):
        alpha[i][0] = start_probabilities[i] * emission_probabilities[i][observations[0]]

    # Induction
    for t in range(1, n_observations):
        for j in range(n_states):
            alpha[j][t] = sum(alpha[i][t - 1] * transition_probabilities[i][j] * emission_probabilities[j][observations[t]] for i in range(n_states))

    return alpha

def backward_algorithm(observations, states, start_probabilities, transition_probabilities, emission_probabilities):
    n_states = len(states)
    n_observations = len(observations)
    beta = np.zeros((n_states, n_observations))

    # Initialization
    for i in range(n_states):
        beta[i][n_observations - 1] = 1  # β(T) = 1 for all states

    # Induction
    for t in range(n_observations - 2, -1, -1):
        for i in range(n_states):
            beta[i][t] = sum(transition_probabilities[i][j] * emission_probabilities[j][observations[t + 1]] * beta[j][t + 1] for j in range(n_states))

    return beta

def baum_welch(observations, states, start_probabilities, transition_probabilities, emission_probabilities, max_iterations=100, tol=1e-4):
    n_states = len(states)
    n_observations = len(observations)
    num_observations = len(observations)

    # Convert lists to numpy arrays for easier manipulation
    start_probabilities = np.array(start_probabilities)
    transition_probabilities = np.array(transition_probabilities)
    emission_probabilities = np.array(emission_probabilities)

    for _ in range(max_iterations):
        # E-step: Compute forward and backward probabilities
        alpha = forward_algorithm(observations, states, start_probabilities, transition_probabilities, emission_probabilities)
        beta = backward_algorithm(observations, states, start_probabilities, transition_probabilities, emission_probabilities)

        # Compute the probability of the observation sequence
        prob_observation = sum(alpha[i][-1] for i in range(n_states))

        # Compute the expected number of transitions and emissions
        xi = np.zeros((n_states, n_states, num_observations - 1))
        for t in range(num_observations - 1):
            denominator = sum(alpha[i][t] * transition_probabilities[i][j] * emission_probabilities[j][observations[t + 1]] * beta[j][t + 1] for i in range(n_states) for j in range(n_states))
            for i in range(n_states):
                for j in range(n_states):
                    numerator = alpha[i][t] * transition_probabilities[i][j] * emission_probabilities[j][observations[t + 1]] * beta[j][t + 1]
                    xi[i][j][t] = numerator / denominator

        # Update transition probabilities
        transition_probabilities_new = np.sum(xi, axis=2) / np.sum(xi.sum(axis=1), axis=1, keepdims=True)

        # Update emission probabilities
        for j in range(n_states):
            for k in range(emission_probabilities.shape[1]):
                numerator = sum(xi[j][:, t].sum() for t in range(num_observations) if observations[t] == k)
                denominator = sum(xi[j][:, t].sum() for t in range(num_observations))
                emission_probabilities[j][k] = numerator / denominator if denominator > 0 else emission_probabilities[j][k]

        # Update start probabilities
        start_probabilities_new = alpha[:, 0] * beta[:, 0] / prob_observation

        # Check for convergence
        if np.max(np.abs(transition_probabilities - transition_probabilities_new)) < tol and np.max(np.abs(emission_probabilities - emission_probabilities)) < tol:
            break

        # Update probabilities
        transition_probabilities = transition_probabilities_new
        start_probabilities = start_probabilities_new

    return start_probabilities, transition_probabilities, emission_probabilities

# Example usage
if __name__ == "__main__":
    # Define parameters
    observations = [0, 1, 0]  # e.g., o_1 = 0, o_2 = 1, o_3 = 0
    states = [0, 1]  # e.g., S_1 = 0, S_2 = 1
    start_probabilities = np.array([0.6, 0.4])  # Initial probabilities
    transition_probabilities = np.array([[0.7, 0.3],  # Transition probabilities
                                         [0.4, 0.6]])
    emission_probabilities = np.array([[0.5, 0.5],  # Emission probabilities for state 0
                                        [0.1, 0.9]])  # Emission probabilities for state 1

    # Train HMM using Baum-Welch algorithm
    start_probabilities, transition_probabilities, emission_probabilities = baum_welch(observations, states, start_probabilities, transition_probabilities, emission_probabilities)

    print("Updated Start Probabilities:", start_probabilities)
    print("Updated Transition Probabilities:", transition_probabilities)
    print("Updated Emission Probabilities:", emission_probabilities)
