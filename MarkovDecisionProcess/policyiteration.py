import numpy as np

class MDP_PolicyIteration:
    def __init__(self, states, actions, transition_probs, rewards, discount_factor=0.9):
        self.states = states
        self.actions = actions
        self.transition_probs = transition_probs
        self.rewards = rewards
        self.discount_factor = discount_factor

    def policy_iteration(self):
        policy = np.zeros(len(self.states), dtype=int)
        value_function = np.zeros(len(self.states))

        while True:
            # Policy Evaluation
            while True:
                delta = 0
                for s in range(len(self.states)):
                    v = value_function[s]
                    value_function[s] = sum(self.transition_probs[s, policy[s], s_next] *
                                             (self.rewards[s, policy[s]] + self.discount_factor * value_function[s_next])
                                             for s_next in range(len(self.states)))
                    delta = max(delta, abs(v - value_function[s]))
                if delta < 1e-6:
                    break

            # Policy Improvement
            policy_stable = True
            for s in range(len(self.states)):
                old_action = policy[s]
                policy[s] = np.argmax([sum(self.transition_probs[s, a, s_next] *
                                            (self.rewards[s, a] + self.discount_factor * value_function[s_next])
                                            for s_next in range(len(self.states)))
                                       for a in range(len(self.actions))])
                if old_action != policy[s]:
                    policy_stable = False

            if policy_stable:
                break

        return policy, value_function

def test_mdp_policy_iteration():
    # Define a small MDP example with known optimal policy for testing
    states = [0, 1]
    actions = [0, 1]
    transition_probs = np.array([
        [[0.8, 0.2], [0.1, 0.9]],  # Transitions from state 0
        [[0.7, 0.3], [0.4, 0.6]]   # Transitions from state 1
    ])
    rewards = np.array([
        [5, 10],  # Rewards for actions in state 0
        [1, 2]    # Rewards for actions in state 1
    ])
    discount_factor = 0.9
    mdp_policy = MDP_PolicyIteration(states, actions, transition_probs, rewards, discount_factor)

    # Run the policy iteration
    optimal_policy, optimal_value_function = mdp_policy.policy_iteration()

    # Expected values (these should be updated based on the specific MDP setup)
    expected_policy = np.array([1, 1])  # Hypothetical optimal policy
    expected_value_function = np.array([15, 10])  # Hypothetical value function

    # Test 1: Check the optimal policy
    try:
        assert np.array_equal(optimal_policy, expected_policy), f"Expected policy {expected_policy}, got {optimal_policy}"
        print("Test 1 passed: Optimal policy is correct.")
    except AssertionError as e:
        print("Test 1 failed:", e)

    # Test 2: Check if the policy is stable after convergence
    try:
        policy_changes = sum(optimal_policy != expected_policy)
        assert policy_changes == 0, "Policy did not converge to a stable policy."
        print("Test 2 passed: Policy converges and is stable.")
    except AssertionError as e:
        print("Test 2 failed:", e)

    # Test 3: Check if the value function has converged within a small tolerance
    try:
        assert np.allclose(optimal_value_function, expected_value_function, rtol=1e-5, atol=1e-6), \
            f"Expected value function {expected_value_function}, got {optimal_value_function}"
        print("Test 3 passed: Value function converges correctly.")
    except AssertionError as e:
        print("Test 3 failed:", e)

def main():
    mdp_policy = MDP_PolicyIteration(states, actions, transition_probs, rewards)
    optimal_policy, optimal_value_policy = mdp_policy.policy_iteration()
    print("Optimal Policy:", optimal_policy)
    print("Optimal Value Function:", optimal_value_policy)
    # Test the MDP policy iteration method
    test_mdp_policy_iteration()

if __name__ == '__main__':
    main()