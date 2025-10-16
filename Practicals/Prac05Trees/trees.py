
class DSATreeNode:
    """
    A node for a binary search tree.
    """
    def __init__(self, key, value):
        """
        Initialises a new tree node.
        """
        if key is None: # safety check
            raise ValueError("Key cannot be None")
        self.key = key
        self.value = value
        self.left_child = None # every new
        self.right_child = None

    def __str__(self):
        # user friendly output string to show node's key and value. 
        return f"Key: {self.key}, Value: {self.value}" 

class DSABinarySearchTree:
    """
    A binary search tree implementation.
    """
    def __init__(self):
        """
        initialises an empty binary search tree.
        """
        self.root = None

    def find(self, key):
        """Finds a value in the tree by its key."""
        return self._find_rec(key, self.root)

    def _find_rec(self, key, current_node):
        """
        Private method to recursively find a value in the tree.
        """
        if current_node is None: # base case
            raise ValueError(f"Key {key} not found")
        elif key == current_node.key: # 2nd base case
            return current_node.value
        elif key < current_node.key:
            return self._find_rec(key, current_node.left_child)
        else:
            return self._find_rec(key, current_node.right_child)

    def insert(self, key, value):
        """ Inserts a new node into the tree."""
        self.root = self._insert_rec(key, value, self.root)

    def _insert_rec(self, key, value, current_node):
        """Recursively inserts a new node into the tree."""
        if current_node is None:
            current_node = DSATreeNode(key, value)
        elif key == current_node.key:
            raise ValueError("Key already exists in the tree")
        elif key < current_node.key:
            current_node.left_child = self._insert_rec(key, value, current_node.left_child)
        else:
            current_node.right_child = self._insert_rec(key, value, current_node.right_child)
        return current_node

    def delete(self, key):
        """
        Deletes a node from the tree by its key.
        """
        self.root = self._delete_rec(key, self.root)

    def _delete_rec(self, key, current_node):
        """
        Recursively deletes a node from the tree.
        """
        if current_node is None:
            raise ValueError("Key not found in tree")
        elif key < current_node.key:
            current_node.left_child = self._delete_rec(key, current_node.left_child)
        elif key > current_node.key:
            current_node.right_child = self._delete_rec(key, current_node.right_child)
        else:
            current_node = self._delete_node(current_node)
        return current_node

    def _delete_node(self, node_to_delete):
        """
        Helper method to handle the three deletion cases.
        """
        if node_to_delete.left_child is None and node_to_delete.right_child is None:
            # Case 1: No children
            return None
        elif node_to_delete.left_child is None:
            # Case 2: One child (right)
            return node_to_delete.right_child
        elif node_to_delete.right_child is None:
            # Case 2: One child (left)
            return node_to_delete.left_child
        else:
            # Case 3: Two children
            successor = self._get_successor(node_to_delete.right_child)
            node_to_delete.key = successor.key
            node_to_delete.value = successor.value
            node_to_delete.right_child = self._delete_rec(successor.key, node_to_delete.right_child)
            return node_to_delete

    def _get_successor(self, current_node):
        """
        Finds the successor of a node (left-most node in the right subtree).
        """
        while current_node.left_child is not None:
            current_node = current_node.left_child
        return current_node

    def min(self):
        """
        Finds the minimum key in the tree.
        """
        if self.root is None:
            return None
        current_node = self.root
        while current_node.left_child is not None:
            current_node = current_node.left_child
        return current_node.key

    def max(self):
        """
        Finds the maximum key in the tree.
        """
        if self.root is None:
            return None
        current_node = self.root
        while current_node.right_child is not None:
            current_node = current_node.right_child
        return current_node.key

    def height(self):
        """
        Calculates the height of the tree.
        """
        return self._height_rec(self.root)

    def _height_rec(self, current_node):
        """Recursively calculates the height of the tree. (longest path from root to leaf)"""
        if current_node is None: # base case
            return -1
        else:
            left_height = self._height_rec(current_node.left_child)
            right_height = self._height_rec(current_node.right_child)
            return 1 + max(left_height, right_height)

    def balance(self):
        """
        Calculates the balance factor of the tree. A perfectly balanced tree has a balance factor of 1.0.
        Comapring the heights of left and right subtree from the root. 
        """
        if self.root is None:
            return 1.0
        
        left_height = self._height_rec(self.root.left_child)
        right_height = self._height_rec(self.root.right_child)
        
        # Avoid division by zero for a tree with only a root
        if left_height == -1 and right_height == -1:
             return 1.0
             
        # Calculate balance based on height difference
        return 1.0 - abs(left_height - right_height) / (1.0 + max(left_height, right_height))


    def inorder_traversal(self):
        """
        Performs an inorder traversal of the tree.
        Left subtree, node itslef, right sub tree. 
        Visits nodes in ascending order. 
        """
        result = []
        self._inorder_rec(self.root, result)
        return result

    def _inorder_rec(self, current_node, result):
        """
        Recursively performs an inorder traversal.
        """
        if current_node is not None:
            self._inorder_rec(current_node.left_child, result)
            result.append(current_node.key)
            self._inorder_rec(current_node.right_child, result)

    def preorder_traversal(self):
        """
        Performs a preorder traversal of the tree.
        Node first, left subtree, right subtree. 
        """
        result = []
        self._preorder_rec(self.root, result)
        return result

    def _preorder_rec(self, current_node, result):
        """
        Recursively performs a preorder traversal.
        """
        if current_node is not None:
            result.append(current_node.key) # 1. visit node
            self._preorder_rec(current_node.left_child, result) # 2. go left
            self._preorder_rec(current_node.right_child, result) # 3. Go right

    def postorder_traversal(self):
        """ Performs a post-order traversal of the tree."""
        result = []
        self._postorder_rec(self.root, result)
        return result

    def _postorder_rec(self, current_node, result):
        """
        Recursively performs a postorder traversal. 
        """
        if current_node is not None:
            self._postorder_rec(current_node.left_child, result) # 1. goleft
            self._postorder_rec(current_node.right_child, result) # 2. Go right
            result.append(current_node.key) # 3. Visit node
