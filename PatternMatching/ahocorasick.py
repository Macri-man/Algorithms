class AhoCorasick:
    def __init__(self):
        self.num_nodes = 1  # Start with root node
        self.edges = [{}]   # List of dictionaries to store transitions
        self.fail_links = [-1]  # Failure links
        self.output_links = [[]] # Output links for matches
        self.output = [[]]  # Output for matches

    def add_pattern(self, pattern):
        current_node = 0  # Start at the root
        for char in pattern:
            # If the character is not in the current node's edges
            if char not in self.edges[current_node]:
                # Create a new node
                self.edges[current_node][char] = self.num_nodes
                self.edges.append({})
                self.fail_links.append(-1)
                self.output_links.append([])
                self.output.append([])
                self.num_nodes += 1
            
            # Move to the next node
            current_node = self.edges[current_node][char]
        
        # Add the pattern to the output of the final node
        self.output[current_node].append(pattern)

    def build_failure_links(self):
        from collections import deque
        
        queue = deque()
        
        # Initialize depth 1 nodes
        for char in self.edges[0]:
            node = self.edges[0][char]
            self.fail_links[node] = 0  # Fail link to root
            queue.append(node)
        
        while queue:
            current_node = queue.popleft()
            
            for char, next_node in self.edges[current_node].items():
                # Add child to queue
                queue.append(next_node)
                
                # Find failure link for next_node
                fail_node = self.fail_links[current_node]
                
                while fail_node != -1 and char not in self.edges[fail_node]:
                    fail_node = self.fail_links[fail_node]
                
                # If fail_node is found, set fail link
                if fail_node != -1:
                    self.fail_links[next_node] = self.edges[fail_node][char]
                else:
                    self.fail_links[next_node] = 0
                
                # Add output links for matches
                self.output_links[next_node].extend(self.output[self.fail_links[next_node]])

    def search(self, text):
        current_node = 0
        results = []

        for char in text:
            # Follow fail links until we find a match or reach the root
            while current_node != -1 and char not in self.edges[current_node]:
                current_node = self.fail_links[current_node]
            
            if current_node == -1:
                current_node = 0  # Back to root
            
            # Move to the next node
            current_node = self.edges[current_node].get(char, 0)

            # Collect matches from output
            if self.output[current_node]:
                results.extend(self.output[current_node])
            
            # Check output links for additional matches
            for output_node in self.output_links[current_node]:
                results.extend(output_node)
        
        return results


# Example usage:
if __name__ == "__main__":
    ac = AhoCorasick()
    
    patterns = ["he", "she", "his", "hers"]
    for pattern in patterns:
        ac.add_pattern(pattern)

    ac.build_failure_links()
    
    text = "ushers"
    matches = ac.search(text)
    
    print("Patterns found:", matches)
