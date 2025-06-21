import numpy as np

class HiddenMarkovModel:
    def __init__(self, A, B, pi, states, observations):
        """
        A: Transition probability matrix (NxN)
        B: Emission probability matrix (NxM)
        pi: Initial state distribution vector (N)
        states: list of states
        observations: list of possible observations
        """
        self.A = np.array(A)
        self.B = np.array(B)
        self.pi = np.array(pi)
        self.states = states
        self.observations = observations
        self.N = len(states)      # Number of states
        self.M = len(observations) # Number of observation symbols

    def _obs_index(self, obs):
        return self.observations.index(obs)

    def forward(self, O):
        """
        Forward algorithm to compute P(O | lambda)
        O: observation sequence (list)
        Returns: probability of observing O
        """
        T = len(O)
        alpha = np.zeros((T, self.N))

        # Initialization
        for i in range(self.N):
            alpha[0, i] = self.pi[i] * self.B[i, self._obs_index(O[0])]
        # Recursion
        for t in range(1, T):
            for j in range(self.N):
                alpha[t, j] = np.sum(alpha[t-1, :] * self.A[:, j]) * self.B[j, self._obs_index(O[t])]
        # Termination
        prob = np.sum(alpha[T-1, :])
        return prob, alpha

    def backward(self, O):
        """
        Backward algorithm for computing probabilities (used in Baum-Welch)
        O: observation sequence
        Returns beta matrix
        """
        T = len(O)
        beta = np.zeros((T, self.N))

        # Initialization
        beta[T-1, :] = 1
        # Recursion backward
        for t in reversed(range(T-1)):
            for i in range(self.N):
                beta[t, i] = np.sum(self.A[i, :] * self.B[:, self._obs_index(O[t+1])] * beta[t+1, :])
        return beta

    def viterbi(self, O):
        """
        Viterbi algorithm for decoding the most probable state sequence
        O: observation sequence
        Returns: (best path probability, best path as list of states)
        """
        T = len(O)
        delta = np.zeros((T, self.N))
        psi = np.zeros((T, self.N), dtype=int)

        # Initialization
        for i in range(self.N):
            delta[0, i] = self.pi[i] * self.B[i, self._obs_index(O[0])]
            psi[0, i] = 0

        # Recursion
        for t in range(1, T):
            for j in range(self.N):
                seq_probs = delta[t-1, :] * self.A[:, j]
                psi[t, j] = np.argmax(seq_probs)
                delta[t, j] = np.max(seq_probs) * self.B[j, self._obs_index(O[t])]

        # Termination
        best_prob = np.max(delta[T-1, :])
        best_path_pointer = np.argmax(delta[T-1, :])

        # Path backtracking
        best_path = [best_path_pointer]
        for t in range(T-1, 0, -1):
            best_path.insert(0, psi[t, best_path[0]])

        best_state_path = [self.states[state] for state in best_path]
        return best_prob, best_state_path

    def baum_welch(self, O_seq, max_iter=100, tol=1e-4):
        """
        Baum-Welch algorithm to learn HMM parameters from observation sequences
        O_seq: list of observation sequences (each sequence is a list)
        max_iter: maximum iterations
        tol: convergence threshold on log likelihood
        """
        M = self.M
        N = self.N

        for iteration in range(max_iter):
            A_num = np.zeros_like(self.A)
            A_den = np.zeros(N)
            B_num = np.zeros_like(self.B)
            B_den = np.zeros(N)
            pi_new = np.zeros(N)
            log_likelihood = 0

            for O in O_seq:
                T = len(O)
                alpha = self.forward(O)[1]
                beta = self.backward(O)

                # Compute gamma and xi
                gamma = np.zeros((T, N))
                xi = np.zeros((T-1, N, N))

                for t in range(T):
                    denom = np.sum(alpha[t, :] * beta[t, :])
                    for i in range(N):
                        gamma[t, i] = (alpha[t, i] * beta[t, i]) / denom

                for t in range(T-1):
                    denom = 0
                    for i in range(N):
                        for j in range(N):
                            denom += alpha[t, i] * self.A[i, j] * self.B[j, self._obs_index(O[t+1])] * beta[t+1, j]
                    for i in range(N):
                        for j in range(N):
                            xi[t, i, j] = (alpha[t, i] * self.A[i, j] * self.B[j, self._obs_index(O[t+1])] * beta[t+1, j]) / denom

                # Update initial probabilities
                pi_new += gamma[0, :]

                # Update A
                for i in range(N):
                    for j in range(N):
                        A_num[i, j] += np.sum(xi[:, i, j])
                    A_den[i] += np.sum(gamma[:-1, i])

                # Update B
                for i in range(N):
                    for k in range(M):
                        mask = [1 if obs == self.observations[k] else 0 for obs in O]
                        B_num[i, k] += np.sum(gamma[:, i] * mask)
                    B_den[i] += np.sum(gamma[:, i])

                # Accumulate log likelihood
                log_likelihood += np.log(np.sum(alpha[-1, :]))

            # Normalize and update parameters
            self.pi = pi_new / len(O_seq)
            for i in range(N):
                self.A[i, :] = A_num[i, :] / (A_den[i] if A_den[i] > 0 else 1)
                self.B[i, :] = B_num[i, :] / (B_den[i] if B_den[i] > 0 else 1)

            if iteration > 0 and abs(log_likelihood - old_log_likelihood) < tol:
                break
            old_log_likelihood = log_likelihood

        return self.A, self.B, self.pi

# Example usage:
if __name__ == "__main__":
    states = ['Rainy', 'Sunny']
    observations = ['walk', 'shop', 'clean']

    A = [[0.7, 0.3],
         [0.4, 0.6]]

    B = [[0.1, 0.4, 0.5],
         [0.6, 0.3, 0.1]]

    pi = [0.6, 0.4]

    hmm = HiddenMarkovModel(A, B, pi, states, observations)

    obs_seq = ['walk', 'shop', 'clean']

    prob, alpha = hmm.forward(obs_seq)
    print(f"Probability of the observation sequence: {prob:.5f}")

    best_prob, best_path = hmm.viterbi(obs_seq)
    print(f"Best state path: {best_path} with probability {best_prob:.5f}")

    # Training on multiple sequences example
    sequences = [
        ['walk', 'shop', 'clean'],
        ['walk', 'walk', 'shop'],
        ['shop', 'clean', 'clean']
    ]
    A_new, B_new, pi_new = hmm.baum_welch(sequences, max_iter=10)
    print("Updated Transition Matrix A:\n", A_new)
    print("Updated Emission Matrix B:\n", B_new)
    print("Updated Initial State Distribution pi:\n", pi_new)
