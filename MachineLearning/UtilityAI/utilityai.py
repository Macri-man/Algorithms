import random

class UtilityAI:
    def __init__(self):
        self.health = 100
        self.enemy_distance = 50
        self.resources = 50

    # Utility functions for each action
    def utility_heal(self):
        return max(0, (100 - self.health) * 0.5)  # Healing is more important when health is low

    def utility_attack(self):
        return max(0, (50 - self.enemy_distance) * 1.5)  # Attacking is more important when close to the enemy

    def utility_gather_resources(self):
        return max(0, (100 - self.resources) * 0.7)  # Gathering is more important when resources are low

    # Decision-making based on the utility of each action
    def choose_action(self):
        actions = {
            'heal': self.utility_heal(),
            'attack': self.utility_attack(),
            'gather_resources': self.utility_gather_resources()
        }
        return max(actions, key=actions.get)  # Return the action with the highest utility

    # Method to simulate the effect of performing an action
    def perform_action(self, action):
        if action == 'heal':
            heal_amount = random.randint(10, 30)
            self.health = min(100, self.health + heal_amount)
            print(f"AI chooses to heal. Health increased by {heal_amount}, now at {self.health}.")
        elif action == 'attack':
            damage = random.randint(10, 25)
            self.enemy_distance = max(0, self.enemy_distance - damage)
            print(f"AI chooses to attack. Enemy distance reduced by {damage}, now at {self.enemy_distance}.")
        elif action == 'gather_resources':
            resource_amount = random.randint(10, 25)
            self.resources = min(100, self.resources + resource_amount)
            print(f"AI chooses to gather resources. Resources increased by {resource_amount}, now at {self.resources}.")
        else:
            print(f"AI is confused and does nothing.")

# Main function to run the AI in a loop
def main():
    agent = UtilityAI()

    for _ in range(10):  # Simulate 10 decision-making turns
        print("\n--- New Decision ---")
        action = agent.choose_action()
        agent.perform_action(action)

if __name__ == "__main__":
    main()
