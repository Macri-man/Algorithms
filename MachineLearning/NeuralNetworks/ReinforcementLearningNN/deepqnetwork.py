import numpy as np
import random
import tensorflow as tf
from collections import deque
class SimpleEnvironment:
    def __init__(self, goal_position):
        self.goal_position = goal_position
        self.state_size = 1  # Simple state representation (position)
        self.action_size = 2  # Actions: 0 (left), 1 (right)

    def reset(self):
        self.position = 0  # Start position
        return np.array([self.position])

    def step(self, action):
        if action == 0:  # Move left
            self.position -= 1
        else:  # Move right
            self.position += 1
        
        # Reward structure
        if self.position == self.goal_position:
            return np.array([self.position]), 1, True  # Reward +1 for reaching the goal
        elif self.position < 0:
            return np.array([self.position]), -1, True  # Negative reward for going out of bounds
        else:
            return np.array([self.position]), 0, False  # No reward

    def render(self):
        print(f"Position: {self.position}, Goal: {self.goal_position}")
class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(tf.keras.layers.Dense(24, activation='relu'))
        model.add(tf.keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        return model

    def predict(self, state):
        return self.model.predict(state)

    def fit(self, state, target):
        self.model.fit(state, target, verbose=0)
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = DQN(state_size, action_size)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)  # Explore
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])  # Exploit

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target += self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
if __name__ == "__main__":
    # Initialize environment and agent
    env = SimpleEnvironment(goal_position=5)
    agent = DQNAgent(state_size=env.state_size, action_size=env.action_size)
    episodes = 1000
    batch_size = 32

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, agent.state_size])
        done = False
        total_reward = 0

        while not done:
            action = agent.act(state)  # Choose action
            next_state, reward, done = env.step(action)  # Step in the environment
            next_state = np.reshape(next_state, [1, agent.state_size])
            agent.remember(state, action, reward, next_state, done)  # Store experience
            state = next_state  # Transition to next state
            total_reward += reward

        agent.replay(batch_size)  # Train the agent with experience replay

        if e % 100 == 0:
            print(f"Episode: {e}, Total Reward: {total_reward}, Epsilon: {agent.epsilon:.2f}")
