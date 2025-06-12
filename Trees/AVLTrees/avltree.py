class Node:
    def __init__(self, key):
        self.key = key  # Key of the node
        self.left = None  # Left child
        self.right = None  # Right child
        self.height = 1  # Initial height of node


class AVLTree:
    def __init__(self):
        self.root = None  # Initially, the tree is empty

    # Get the height of the node
    def height(self, node):
        if not node:
            return 0
        return node.height

    # Get the balance factor of the node
    def balanceFactor(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    # Right rotation (used for LL case)
    def rightRotate(self, z):
        y = z.left
        T2 = y.right

        # Perform rotation
        y.right = z
        z.left = T2

        # Update heights
        z.height = max(self.height(z.left), self.height(z.right)) + 1
        y.height = max(self.height(y.left), self.height(y.right)) + 1

        return y  # New root

    # Left rotation (used for RR case)
    def leftRotate(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = max(self.height(z.left), self.height(z.right)) + 1
        y.height = max(self.height(y.left), self.height(y.right)) + 1

        return y  # New root

    # Insert a node into the AVL tree
    def insert(self, root, key):
        # 1. Perform the normal BST insert
        if not root:
            return Node(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # 2. Update height of this ancestor node
        root.height = 1 + max(self.height(root.left), self.height(root.right))

        # 3. Get the balance factor to check whether this node became unbalanced
        balance = self.balanceFactor(root)

        # If this node becomes unbalanced, then there are 4 cases

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self.rightRotate(root)

        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self.leftRotate(root)

        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        # Return the (unchanged) node pointer
        return root

    # Utility function to do inorder traversal of the tree
    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.key, end=" ")
            self.inorder(root.right)

    # Function to insert a node
    def insertKey(self, key):
        self.root = self.insert(self.root, key)

    # Function to visually print the AVL Tree with balance factors
    def printTree(self, node, level=0, prefix="Root: "):
        if node is not None:
            bf = self.balanceFactor(node)
            print(" " * (level * 4) + f"{prefix}{node.key} (BF={bf})")
            if node.left or node.right:
                if node.left:
                    self.printTree(node.left, level + 1, prefix="L--- ")
                else:
                    print(" " * ((level + 1) * 4) + "L--- None")
                if node.right:
                    self.printTree(node.right, level + 1, prefix="R--- ")
                else:
                    print(" " * ((level + 1) * 4) + "R--- None")

# Example usage
if __name__ == "__main__":
    avl = AVLTree()

    # Insert keys
    keys = [-50, 5, -30, 30, 20, 10, 25, 40, 50, 35]
    for key in keys:
        avl.insertKey(key)

    # Inorder traversal
    print("Inorder traversal of AVL tree:")
    avl.inorder(avl.root)
    print("\n")

    # Tree diagram with balance factors
    print("AVL Tree structure with Balance Factors:")
    avl.printTree(avl.root)
