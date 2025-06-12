import numpy as np

class MDP:
    def __init__(self, states, actions, transition_probs, rewards, discount_factor=0.9):
        self.states = states
        self.actions = actions
        self.transition_probs = transition_probs  # P(s'|s,a)
        self.rewards = rewards                      # R(s,a)
        self.discount_factor = discount_factor

    def value_iteration(self, theta=1e-6):
        value_function = np.zeros(len(self.states))
        while True:
            delta = 0
            for s in range(len(self.states)):
                v = value_function[s]
                value_function[s] = max(
                    sum(self.transition_probs[s, a, s_next] * (self.rewards[s, a] + self.discount_factor * value_function[s_next])
                        for s_next in range(len(self.states)))
                    for a in range(len(self.actions))
                )
                delta = max(delta, abs(v - value_function[s]))
            if delta < theta:
                break
        return value_function

class TestMDP:
    @staticmethod
    def run_tests():
        states = [0, 1, 2]  # State space
        actions = [0, 1]    # Action space
        transition_probs = np.array([[[0.8, 0.2, 0.0],  # From state 0
                                       [0.0, 0.8, 0.2]],  # From state 1
                                      [[0.0, 0.2, 0.8],  # From state 2
                                       [0.0, 0.0, 1.0]]])  # From state 2 with action 1
        rewards = np.array([[5, 10],  # Rewards for state 0
                            [0, 1],   # Rewards for state 1
                            [0, 0]])  # Rewards for state 2

        mdp = MDP(states, actions, transition_probs, rewards)
        optimal_value = mdp.value_iteration()
        print("Optimal Value Function:", optimal_value)




def main():
    # Example usage
    states = [0, 1, 2]  # State space
    actions = [0, 1]    # Action space
    transition_probs = np.array([[[0.8, 0.2, 0.0],  # From state 0
                               [0.0, 0.8, 0.2]],  # From state 1
                              [[0.0, 0.2, 0.8],  # From state 2
                               [0.0, 0.0, 1.0]]])  # From state 2 with action 1
    rewards = np.array([[5, 10],  # Rewards for state 0
                    [0, 1],   # Rewards for state 1
                    [0, 0]])  # Rewards for state 2

    mdp = MDP(states, actions, transition_probs, rewards)
    optimal_value = mdp.value_iteration()
    print("Optimal Value Function:", optimal_value)
    TestMDP.run_tests()

if __name__ == "__main__":
    main()