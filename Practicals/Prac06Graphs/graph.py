import collections
from collections import deque

# DSALinkedList remains the same as it's a utility class.
class DSALinkedList:
    class _DSAListNode:
        def __init__(self, value):
            self.value = value
            self.next = None
    def __init__(self):
        self.head = None; self.count = 0
    def insert_last(self, value):
        new_node = self._DSAListNode(value)
        if self.head is None: self.head = new_node
        else:
            curr = self.head
            while curr.next: curr = curr.next
            curr.next = new_node
        self.count += 1
    def __iter__(self):
        curr = self.head
        while curr: yield curr.value; curr = curr.next
    def __len__(self): return self.count
    def remove(self, value):
        prev, curr = None, self.head
        while curr and curr.value != value: prev, curr = curr, curr.next
        if curr is None: return
        if prev is None: self.head = curr.next
        else: prev.next = curr.next
        self.count -= 1

class DSAGraphVertex:
    """
    Represents a single vertex in the graph. Renamed from DSAGraphNode.
    Method names and fields now match the provided class diagram. 
    """
    def __init__(self, inLabel, inValue=None): # CONSTRUCTOR 
        self._label = inLabel
        self._value = inValue
        self.links = DSALinkedList() # Adjacency list is now 'links' 
        self.visited = False

    def getLabel(self): # ACCESSOR 
        return self._label

    def getValue(self): # ACCESSOR 
        return self._value

    def getAdjacent(self): # ACCESSOR 
        return self.links

    def addEdge(self, vertex): # MUTATOR 
        self.links.insert_last(vertex)

    def setVisited(self): # MUTATOR 
        self.visited = True

    def clearVisited(self): # MUTATOR 
        self.visited = False

    def getVisited(self): # ACCESSOR 
        return self.visited

    def toString(self): # ACCESSOR 
        return str(self._label)
    
    def __repr__(self):
        """Makes printing the object call the required toString() method."""
        return self.toString()

class DSAGraph:
    """
    Holds vertices in linked list.
    Each vertex has a label, possible value, and a linked list of neighbours. 
    """
    def __init__(self): # CONSTRUCTOR 
        self.vertices = DSALinkedList()

    def addVertex(self, label, value=None): # MUTATOR 
        if not self.hasVertex(label):
            self.vertices.insert_last(DSAGraphVertex(label, value))

    def addEdge(self, label1, label2): # MUTATOR 
        self.addVertex(label1)
        self.addVertex(label2)
        node1, node2 = self.getVertex(label1), self.getVertex(label2)
        if node1 and node2:
            node1.addEdge(node2)
            node2.addEdge(node1) # For undirected graph 
    
    def hasVertex(self, label): # ACCESSOR 
        return self.getVertex(label) is not None

    def getVertexCount(self): # ACCESSOR
        return len(self.vertices)

    def getEdgeCount(self): # ACCESSOR 
        return sum(len(v.getAdjacent()) for v in self.vertices) // 2

    def getVertex(self, label): # ACCESSOR 
        for vertex in self.vertices:
            if vertex.getLabel() == label:
                return vertex
        return None

    def getAdjacent(self, label): # ACCESSOR 
        vertex = self.getVertex(label)
        if vertex:
            return vertex.getAdjacent()
        return DSALinkedList() # Return an empty list if vertex not found

    def isAdjacent(self, label1, label2): # ACCESSOR [cite: 2, 3]
        node1 = self.getVertex(label1)
        if node1:
            for neighbor in node1.getAdjacent():
                if neighbor.getLabel() == label2:
                    return True
        return False

    def displayAsList(self): # ACCESSOR [cite: 2, 3]
        print("\n--- Adjacency List ---")
        for vertex in self.vertices:
            adj_str = " -> ".join([n.toString() for n in vertex.getAdjacent()])
            print(f"{vertex.getLabel()} | {adj_str}")
        print("\n")

    def displayAsMatrix(self): # ACCESSOR [cite: 2, 3]
        print("\n--- Adjacency Matrix ---")
        labels = sorted([v.getLabel() for v in self.vertices])
        print("  " + " ".join(labels))
        for row_label in labels:
            row_str = f"{row_label} "
            for col_label in labels:
                row_str += "1 " if self.isAdjacent(row_label, col_label) else "0 "
            print(row_str.strip())
        print("\n")
    
    def deleteEdge(self, label1, label2):
        node1, node2 = self.getVertex(label1), self.getVertex(label2)
        if not (node1 and node2 and self.isAdjacent(label1, label2)):
            print(f"Error: Edge between '{label1}' and '{label2}' does not exist.")
            return
        node1.getAdjacent().remove(node2)
        node2.getAdjacent().remove(node1)
        print(f"Edge between '{label1}' and '{label2}' deleted.")

    def deleteVertex(self, label):
        vertex_to_delete = self.getVertex(label)
        if not vertex_to_delete:
            print(f"Error: Vertex '{label}' not found.")
            return
        # First, remove all edges connected to this vertex
        for vertex in self.vertices:
            if vertex != vertex_to_delete:
                vertex.getAdjacent().remove(vertex_to_delete)
        # Then, remove the vertex itself from the main list
        self.vertices.remove(vertex_to_delete)
        print(f"Vertex '{label}' and all its edges have been deleted.")
    
    ### SEARCH METHODS ###
    def breadthFirstSearch(self):
        self.clear_visited_flags()
        T = collections.deque()
        Q = collections.deque()

        if self.getVertexCount() == 0: return []

        v = self.getVertex(sorted([vertex.getLabel() for vertex in self.vertices])[0])
        
        v.setVisited()
        Q.append(v)

        while Q:
            v = Q.popleft()
            neighbors = sorted(v.getAdjacent(), key=lambda node: node.getLabel())
            
            for w in neighbors:
                if not w.getVisited():
                    T.append((v.getLabel(), w.getLabel()))
                    w.setVisited()
                    Q.append(w)
                    
        return list(T)

    def depthFirstSearch(self):
        self.clear_visited_flags()
        T = collections.deque()
        S = []

        if self.getVertexCount() == 0: return []

        start_node = self.getVertex(sorted([v.getLabel() for v in self.vertices])[0])
        start_node.setVisited()
        S.append(start_node)

        while S:
            v = S[-1]
            w = self.get_next_unvisited_neighbor(v)
            if w:
                T.append((v.getLabel(), w.getLabel()))
                w.setVisited()
                S.append(w)
            else:
                S.pop()
        return list(T)

    # --- Internal Helper Methods ---

    def clear_visited_flags(self):
        """Helper to reset visited flags on all vertices before a traversal."""
        for vertex in self.vertices:
            vertex.clearVisited()

    def get_next_unvisited_neighbor(self, vertex):
        """Helper for DFS to find the next alphabetically sorted, unvisited neighbor."""
        neighbors = sorted(vertex.getAdjacent(), key=lambda node: node.getLabel())
        for neighbor in neighbors:
            if not neighbor.getVisited():
                return neighbor
        return None

# NOTE: Place this main function at the end of your file, after all class definitions.

def main():
    """Interactive menu with updated method calls."""
    graph = DSAGraph()
    
    # Sample graph to start with
    edges = [('A', 'B'), ('A', 'D'), ('B', 'E'), ('C', 'D'), 
             ('D', 'F'), ('E', 'F'), ('F', 'G')]
    for v1, v2 in edges:
        graph.addEdge(v1, v2)
    print("Sample graph loaded.")

    choice = -1
    while choice != 0:
        print("\n--- Graph Operations Menu ---")
        print("1. Add Node (Vertex)")
        print("2. Delete Node (Vertex)")
        print("3. Add Edge")
        print("4. Delete Edge")
        print("5. Display as List")
        print("6. Display as Matrix")
        print("7. Breadth-First Search")
        print("8. Depth-First Search")
        print("0. Exit")
        
        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                label = input("Enter label for the new node: ").strip().upper()
                graph.addVertex(label)
                print(f"Node '{label}' added.")
            
            elif choice == 2:
                label = input("Enter label of the node to delete: ").strip().upper()
                graph.deleteVertex(label)

            elif choice == 3:
                labels = input("Enter two labels for the edge, separated by a space (e.g., A B): ").strip().upper().split()
                if len(labels) == 2:
                    graph.addEdge(labels[0], labels[1])
                    print(f"Edge between '{labels[0]}' and '{labels[1]}' added.")
                else:
                    print("Invalid input. Please provide two labels.")

            elif choice == 4:
                labels = input("Enter two labels for the edge to delete, separated by a space (e.g., A B): ").strip().upper().split()
                if len(labels) == 2:
                    graph.deleteEdge(labels[0], labels[1])
                else:
                    print("Invalid input. Please provide two labels.")

            elif choice == 5:
                graph.displayAsList()
            
            elif choice == 6:
                graph.displayAsMatrix()

            elif choice == 7:
                path = graph.breadthFirstSearch()
                print("Breadth-First Search Path:", path)

            elif choice == 8:
                path = graph.depthFirstSearch()
                print("Depth-First Search Path:", path)

            elif choice == 0:
                print("Exiting program.")
            
            else:
                print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()