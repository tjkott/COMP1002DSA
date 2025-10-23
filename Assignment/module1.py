import sys # Used for representing infinity in Dijkstra's algorithm

# MODULE 1: Graph-Based Hospital Navigation


# Sources:
## Task 2, bullet 3. 
"""Source: Ihechikara. (2022, November 30). Dijkstra's algorithm – 
        Explained with a pseudocode example. freeCodeCamp. https://www.freecodecamp.org/news/dijkstras-algorithm-explained-with-a-pseudocode-example/"""

class DSALinkedList:
    """
    A custom implementation of a Linked List to avoid using restricted built-in list types.
    This structure is fundamental for building the adjacency lists in the graph.
    """
    class DSAListNode:
        """Inner class representing a node in the linked list."""
        def __init__(self, value):
            self.value = value
            self.next = None

    def __init__(self):
        """Constructor for the linked list."""
        self.head = None
        self.count = 0

    def insertLast(self, value):
        """Adds a new node to the end of the list."""
        new_node = self.DSAListNode(value)
        if self.isEmpty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.count += 1

    def removeFirst(self):
        """Removes and returns the first node's value from the list."""
        if self.isEmpty():
            raise IndexError("Cannot remove from an empty list.")
        value = self.head.value
        self.head = self.head.next
        self.count -= 1
        return value

    def isEmpty(self):
        """Checks if the list is empty."""
        return self.head is None

    def __iter__(self):
        """Makes the linked list iterable."""
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __len__(self):
        """Returns the number of items in the list."""
        return self.count

class DSAQueue:
    """
    A custom Queue implementation using the DSALinkedList.
    This is required for the Breadth-First Search algorithm.
    """
    def __init__(self):
        self._list = DSALinkedList()

    def enqueue(self, value):
        """Adds an item to the back of the queue."""
        self._list.insertLast(value)

    def dequeue(self):
        """Removes and returns the item from the front of the queue."""
        return self._list.removeFirst()

    def isEmpty(self):
        """Checks if the queue is empty."""
        return self._list.isEmpty()

# -------------------------------------------------------------------------------------
# Graph Implementation
# -------------------------------------------------------------------------------------

class DSAGraphVertex: # represents a single "department". 
    """
    Each node in the graph corresponds to a department in the hospital. 
    Each vertex/node possess a label and an adjacency list of its connections.
    """
    def __init__(self, label):
        self.label = label
        self.links = DSALinkedList() # Gives each vertex in graph its own linked list sto store neighbours and edge weights. 
        self.visited = False
        self.distance = sys.maxsize # Contructors for Dijkstra's Algorith
        self.predecessor = None

    def getLabel(self):
        return self.label

    def getAdjacent(self):
        return self.links

    def addEdge(self, neighbor_vertex, weight):
        """Adds a weighted connection to a neighboring vertex."""
        self.links.insertLast((neighbor_vertex, weight))

    def setVisited(self):
        self.visited = True

    def clearVisited(self):
        self.visited = False

    def getVisited(self):
        return self.visited

    def __str__(self):
        return str(self.label)

class DSAGraph: ## Task 1, bullet 1: Implement a graph class. 
    """
    Represents the hospital layout as a weighted, undirected graph.
    Graph uses an adjacency list implemented with the handwritten DSALinkedList class. 
    """
    def __init__(self):
        self._vertices = DSALinkedList()

    def addVertex(self, label): ## Support dynamic insertion of departments (nodes) and corridors (weighted edges).
        """Adds a new department (vertex) to the graph if it doesn't already exist."""
        if not self.hasVertex(label):
            new_vertex = DSAGraphVertex(label)
            self._vertices.insertLast(new_vertex)

    def addEdge(self, label1, label2, weight): ## Ensure undirected symmetry (u↔v with same weight). i.e. connection goes both ways/ 
        """Adds a weighted, undirected corridor (edge) between two departments."""
        self.addVertex(label1)
        self.addVertex(label2)
        v1 = self.getVertex(label1) 
        v2 = self.getVertex(label2)
        v1.addEdge(v2, weight)
        v2.addEdge(v1, weight) # Ensure symmetry for undirected graph

    def getVertex(self, label):
        """Retrieves a vertex object by its label."""
        for vertex in self._vertices:
            if vertex.getLabel() == label:
                return vertex
        return None

    def hasVertex(self, label):
        """Checks if a vertex with the given label exists."""
        return self.getVertex(label) is not None

    def ClearAllVisited(self):
        """Helper method to reset the visited status of all vertices."""
        for vertex in self._vertices:
            vertex.clearVisited()

    def displayAsList(self): ## Textual/visual graph structure. 
        """Displays the graph structure as an adjacency list with weights."""
        print("\n--- Hospital Adjacency List ---")
        for vertex in self._vertices:
            adj_list = []
            for neighbor, weight in vertex.getAdjacent():
                adj_list.append(f"{neighbor.getLabel()}({weight})")
            
            # Manual join to avoid using restricted built-ins
            adj_str = ""
            for i, item in enumerate(adj_list):
                adj_str += item
                if i < len(adj_list) - 1:
                    adj_str += " -> "
            
            print(f"{vertex.getLabel():<18} | {adj_str}")
        print("---------------------------------")

    # --- Core Algorithms ---

    def breadthFirstSearch(self, start_label): ## Breadth-First Search (BFS)
        """
        Performs a Breadth-First Search (BFS) from a starting department.
        Outputs all reachable departments grouped by their level (number of hops).
        """
        print(f"\n--- BFS starting from '{start_label}' ---")
        self.ClearAllVisited()
        start_vertex = self.getVertex(start_label)

        if not start_vertex:
            print(f"Error: Department '{start_label}' not found.")
            return

        q = DSAQueue() # use custom implemented queue. 
        q.enqueue(start_vertex) 
        start_vertex.setVisited()

        # Using a None marker in the queue to separate levels
        q.enqueue(None) 
        level = 0
        
        level_output = f"{start_vertex.getLabel()}"

        while not q.isEmpty():
            current_vertex = q.dequeue()

            if current_vertex is None: 
                print(f"Level {level}: {level_output}")
                level_output = ""
                level += 1
                if not q.isEmpty():
                    q.enqueue(None)
            else:
                for neighbor, _ in current_vertex.getAdjacent():
                    if not neighbor.getVisited():
                        neighbor.setVisited()
                        q.enqueue(neighbor)
                        if level_output == "":
                            level_output += f"{neighbor.getLabel()}"
                        else:
                            level_output += f", {neighbor.getLabel()}"

    def depthFirstSearchCycleFind(self): ## DFS cycle detection (and cycle members if present). 
        """
        Performs a Depth-First Search (DFS) across the entire graph to detect cycles.
        Returns the first cycle found and the nodes involved.
        """
        self.ClearAllVisited()
        # Using lists as sets to track visited nodes and the current path (recursion stack)
        visited = [] 
        recursion_stack = [] # tracks nodes in the path. 
        cycle_found = False

        for vertex in self._vertices:
            if vertex not in visited:
                cycle_path = self.DfsCycleHelper(vertex, visited, recursion_stack)
                if cycle_path:
                    # Manually reverse and format the cycle path for printing
                    reversed_path = []
                    for node in cycle_path:
                        reversed_path.insert(0, str(node))
                    
                    path_str = ""
                    for i, node_label in enumerate(reversed_path):
                        path_str += node_label
                        if i < len(reversed_path) - 1:
                            path_str += " -> "
                    
                    print(f"Cycle Detected: {path_str}")
                    cycle_found = True
                    break # Stop after finding the first cycle
        
        if not cycle_found:
            print("No cycles were found in the hospital layout.")
        print("---------------------------")


    def DfsCycleHelper(self, vertex, visited, recursionstack):
        """Recursive helper for depthFirstSearchCycleFind function"""
        visited.append(vertex)
        recursionstack.append(vertex) 

        for neighbor, _ in vertex.getAdjacent():
            if neighbor not in visited:
                # Recurse and propagate the cycle path if found
                path = self.DfsCycleHelper(neighbor, visited, recursionstack)
                if path:
                    return path
            elif neighbor in recursionstack:
                # Cycle detected. Find where it starts and build the path.
                cycle_start_index = 0
                for i, node in enumerate(recursionstack):
                    if node == neighbor:
                        cycle_start_index = i
                        break
                
                # Build path from the start of the cycle to the current node
                path = [neighbor]
                for i in range(cycle_start_index + 1, len(recursionstack)):
                    path.append(recursionstack[i])
                path.append(neighbor) # Close the loop
                return path

        recursionstack.pop() # Backtrack
        return None

    def dijkstraAlgorithm(self, start_label, end_label):
        ## Shortest Path Algorithm: Implement Dijkstra algorithm from a source; report
        # path and total cost. Cite the algorithm source and implement from first principles
        # without built-in shortest-path functions.
        """
        Dijkstra's algorithm. 
        """
        print(f"\n--- Shortest Path from '{start_label}' to '{end_label}' ---")
        for vertex in self._vertices: # reset distance and predecessor node for all vertices. 
            vertex._distance = sys.maxsize
            vertex._predecessor = None
        
        start_vertex = self.getVertex(start_label)
        end_vertex = self.getVertex(end_label)

        if not start_vertex or not end_vertex:
            print("Error: One or both departments not found.")
            return

        start_vertex._distance = 0
        unvisited = list(self._vertices) # Create a list of all vertices which need to be visted. 

        while unvisited:
            # Find vertex with smallest distance (manual priority queue)
            current_vertex = None
            min_dist = sys.maxsize
            for vertex in unvisited:
                if vertex._distance < min_dist:
                    min_dist = vertex._distance
                    current_vertex = vertex

            if current_vertex is None or current_vertex._distance == sys.maxsize:
                break # No path to remaining nodes

            # Manual removal from list to avoid restricted built-ins
            temp_unvisited = []
            for vertex in unvisited:
                if vertex != current_vertex:
                    temp_unvisited.append(vertex)
            unvisited = temp_unvisited
            
            # Relaxation step
            for neighbor, weight in current_vertex.getAdjacent():
                new_dist = current_vertex._distance + weight
                if new_dist < neighbor._distance:
                    neighbor._distance = new_dist
                    neighbor._predecessor = current_vertex

        # Reconstruct and print path
        if end_vertex._distance == sys.maxsize:
            print(f"No path found from '{start_label}' to '{end_label}'.")
        else:
            path = []
            current = end_vertex
            while current is not None:
                path.insert(0, current.getLabel())
                current = current._predecessor
            
            path_str = ""
            for i, node_label in enumerate(path):
                path_str += node_label
                if i < len(path) - 1:
                    path_str += " -> "
            
            print(f"Path: {path_str}")
            print(f"Total walking time: {end_vertex._distance} minutes.")
        print("\n")

def main():
    """Sets up the hospital graph and provides a menu to test the algorithms."""
    hospital_graph = DSAGraph()

    ## 3) Test Case Setup
    # 8+ departments, 10-12 edges, one cycle, one isolated department.
    departments = ["Emergency", "ICU", "Pharmacy", "Radiology", "Laboratories",
    "Operating Theatres", "Wards", "Outpatient Units", "Cafeteria"] ## At least 8 departments (nodes). 
    for dept in departments:
        hospital_graph.addVertex(dept)
    
    hospital_graph.addVertex("Morgue") ## and one isolated department. 
    ## 10-12 weighted corridors (edges).
    corridors = [("Emergency", "ICU", 4), ## Include at least one cycle
        ("Emergency", "Radiology", 2),
        ("Emergency", "Wards", 7),
        ("ICU", "Operating Theatres", 2),
        ("ICU", "Pharmacy", 3), 
        ("Radiology", "Laboratories", 3),
        ("Laboratories", "Pharmacy", 2),
        ("Operating Theatres", "Wards", 2),
        ("Wards", "Outpatient Units", 5),
        ("Wards", "Cafeteria", 3),
        ("Outpatient Units", "Cafeteria", 2)]
    
    for dept1, dept2, time in corridors:
        hospital_graph.addEdge(dept1, dept2, time)

    print("Module 1: Graph-Based Hospital Navigation")
    
    # Task 4: Expected Output
    # Display the constructed graph
    hospital_graph.displayAsList()

    # Run BFS from 'Emergency'
    hospital_graph.breadthFirstSearch("Emergency")

    # Run DFS to find cycles
    hospital_graph.depthFirstSearchCycleFind()

    # Find and display a shortest path
    hospital_graph.dijkstraAlgorithm("Emergency", "Outpatient Units")
    
    # Example with no path
    hospital_graph.dijkstraAlgorithm("Emergency", "Morgue")

if __name__ == "__main__":
    main()