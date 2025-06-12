import numpy as np

# Mock MDP class to serve as the base for QLearning
class MDP:
    def __init__(self, states, actions, transition_probs, rewards, discount_factor=0.9):
        self.states = states
        self.actions = actions
        self.transition_probs = transition_probs
        self.rewards = rewards
        self.discount_factor = discount_factor

class QLearning(MDP):
    def __init__(self, states, actions, transition_probs, rewards, alpha=0.1, epsilon=0.1, discount_factor=0.9):
        super().__init__(states, actions, transition_probs, rewards, discount_factor)
        self.alpha = alpha
        self.epsilon = epsilon
        # Initialize Q-values as zeros
        self.q_values = np.zeros((len(states), len(actions)))

    def choose_action(self, state):
        # Exploration vs. Exploitation
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)  # Explore: random action
        return np.argmax(self.q_values[state])  # Exploit: choose best action

    def learn(self, episodes=1000):
        for _ in range(episodes):
            state = np.random.choice(self.states)  # Randomly start from any state
            while True:
                action = self.choose_action(state)
                # Transition to the next state based on the transition probabilities
                next_state = np.random.choice(self.states, p=self.transition_probs[state, action])
                reward = self.rewards[state, action]
                
                # Update Q-value using the Bellman equation
                best_next_action = np.argmax(self.q_values[next_state])  # Best action for next state
                self.q_values[state, action] += self.alpha * (reward + self.discount_factor * self.q_values[next_state, best_next_action] - self.q_values[state, action])
                
                # Transition to next state
                state = next_state
                if self.is_terminal_state(state):  # Check for terminal state
                    break

    def is_terminal_state(self, state):
        # Check if the current state is terminal (can be overridden for more complex MDPs)
        return state == len(self.states) - 1

class TestQLearning:
    def __init__(self):
        self.states = [0, 1, 2]  # States
        self.actions = [0, 1]     # Actions (0: left, 1: right)
        
        # Transition probabilities: For simplicity, we'll use deterministic transitions
        # P[state, action] -> next state probability
        self.transition_probs = np.array([
            [[0.0, 1.0], [0.0, 1.0]],  # From state 0: action 0 -> state 0, action 1 -> state 1
            [[0.0, 1.0], [0.0, 1.0]],  # From state 1: action 0 -> state 1, action 1 -> state 2
            [[0.0, 1.0], [0.0, 1.0]],  # From state 2: action 0 -> state 2, action 1 -> terminal state (state 2)
        ])

        # Rewards: assume positive reward for reaching the terminal state
        self.rewards = np.array([
            [0, 1],  # From state 0: action 0 -> reward 0, action 1 -> reward 1
            [0, 1],  # From state 1: action 0 -> reward 0, action 1 -> reward 1
            [0, 0],  # From state 2: action 0 -> reward 0, action 1 -> reward 0
        ])

    def run_test(self):
        q_learning = QLearning(self.states, self.actions, self.transition_probs, self.rewards)
        
        # Train the Q-learning agent
        q_learning.learn(episodes=1000)

        # Test: Check if Q-values are updated for a few states and actions
        print("Learned Q-values:")
        print(q_learning.q_values)
        
        # Assert that Q-values for terminal state do not change
        assert np.all(q_learning.q_values[2, :] == 0), "Q-values for terminal state should be 0."

        # Assert that Q-values for state 0 are non-zero after learning
        assert np.any(q_learning.q_values[0, :] > 0), "Q-values for state 0 should be updated."

        # Assert that action selection is valid
        chosen_action = q_learning.choose_action(0)
        assert chosen_action in self.actions, "Chosen action should be valid."

        print("Test passed successfully.")


def main():

    # Run the test
    test = TestQLearning()
    test.run_test()

    # Example usage
    q_learning = QLearning(states, actions, transition_probs, rewards)
    q_learning.learn()
    print("Learned Q-values:", q_learning.q_values)

if __name__ == '__main__':
    main()
