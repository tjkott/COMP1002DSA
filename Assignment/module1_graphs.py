# MODULE 2: Hash-Based Patient Lookup
# Author: Thejana Kottawatta (22307822)

# Sources:
## Task 2, bullet 3. 
"""Source: Ihechikara. (2022, November 30). Dijkstra's algorithm – 
        Explained with a pseudocode example. freeCodeCamp. https://www.freecodecamp.org/news/dijkstras-algorithm-explained-with-a-pseudocode-example/"""

import sys # Used for representing infinity in Dijkstra's algorithm
import csv
import os
from contextlib import redirect_stdout


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

    # ADDED: insertFirst, needed for path reconstruction without built-in list.insert(0,...)
    def insertFirst(self, value):
        """Adds a new node to the start of the list."""
        new_node = self.DSAListNode(value)
        new_node.next = self.head
        self.head = new_node
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
        self.in_recursion_stack = False

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

    def ClearAllFlags(self):
        """Helper method to reset all flags on all vertices."""
        for vertex in self._vertices:
            vertex.clearVisited()
            vertex.in_recursion_stack = False

    def displayAsList(self): ## Textual/visual graph structure. 
        """Displays the graph structure as an adjacency list with weights."""
        print("\n--- Hospital Adjacency List ---", flush=True)
        for vertex in self._vertices:
            adj_str = ""
            count = 0
            for neighbor, weight in vertex.getAdjacent():
                adj_str += f"{neighbor.getLabel()}({weight})"
                count += 1
                if count < len(vertex.getAdjacent()):
                    adj_str += " -> "
            
            print(f"{vertex.getLabel():<18} | {adj_str}", flush=True)

    def breadthFirstSearch(self, start_label): ## Breadth-First Search (BFS)
        """
        Performs a Breadth-First Search (BFS) from a starting department.
        Outputs all reachable departments grouped by their level (number of hops).
        """
        print(f"\n--- BFS starting from '{start_label}' ---", flush=True)
        self.ClearAllFlags()
        start_vertex = self.getVertex(start_label)

        if not start_vertex:
            print(f"Error: Department '{start_label}' not found.", flush=True)
            return

        q = DSAQueue() # use custom implemented queue. 
        q.enqueue(start_vertex) 
        start_vertex.setVisited()

        # Using a None marker in the queue to separate levels
        q.enqueue(None) 
        level = 0
        
        level_output = ""

        while not q.isEmpty():
            current_vertex = q.dequeue()

            if current_vertex is None: 
                print(f"Level {level}: {level_output}", flush=True)
                level_output = ""
                level += 1
                if not q.isEmpty():
                    q.enqueue(None)
            else:
                if level_output == "":
                    level_output += f"{current_vertex.getLabel()}"
                else:
                    level_output += f", {current_vertex.getLabel()}"
                for neighbor, _ in current_vertex.getAdjacent():
                    if not neighbor.getVisited():
                        neighbor.setVisited()
                        q.enqueue(neighbor)

    def depthFirstSearchCycleFind(self): ## DFS cycle detection (and cycle members if present). 
        """
        Performs a Depth-First Search (DFS) across the entire graph to detect cycles.
        Returns the first cycle found and the nodes involved.
        """
        print("\n--- DFS Cycle Detection ---", flush=True)
        self.ClearAllFlags()
        cycle_found = False
        for vertex in self._vertices:
            if not vertex.getVisited():
                if self.DfsCycleHelper(vertex, None): # Start with no parent
                    cycle_found = True
                    break # Stop after finding the first cycle
        
        if not cycle_found:
            print("No cycles were found in the hospital layout.", flush=True)
        print(" ", flush=True)

    def DfsCycleHelper(self, vertex, parent):
        """
        Recursive helper for DFS cycle detection.
        Uses vertex flags instead of restricted lists.
        """
        vertex.setVisited()
        vertex.in_recursion_stack = True 

        for neighbor, _ in vertex.getAdjacent():
            if neighbor == parent:
                continue 

            if not neighbor.getVisited():
                # Recurse and propagate the cycle-found signal
                if self.DfsCycleHelper(neighbor, vertex): # Pass self as new parent
                    return True
            elif neighbor.in_recursion_stack:
                # We've found a neighbor that is *already* in our current path
                print(f"Cycle Detected: Path found from {vertex.getLabel()} back to {neighbor.getLabel()}", flush=True)
                return True

        vertex.in_recursion_stack = False # Backtrack (remove from recursion stack)
        return False

    def dijkstraAlgorithm(self, start_label, end_label):
        ## Shortest Path Algorithm: Implement Dijkstra algorithm from a source; report
        # path and total cost. Cite the algorithm source and implement from first principles
        # without built-in shortest-path functions.
        """
        Dijkstra's algorithm. 
        """
        print(f"\n--- Shortest Path from '{start_label}' to '{end_label}' ---", flush=True)
        for vertex in self._vertices: # reset distance and predecessor node for all vertices. 
            vertex._distance = sys.maxsize
            vertex._predecessor = None
            vertex.clearVisited() # Use visited flag for Dijkstra
        
        start_vertex = self.getVertex(start_label)
        end_vertex = self.getVertex(end_label)

        if not start_vertex or not end_vertex:
            print("Error: One or both departments not found.", flush=True)
            return

        start_vertex._distance = 0
        
        unvisited_count = len(self._vertices) 

        while unvisited_count > 0:
            current_vertex = None
            min_dist = sys.maxsize
            for vertex in self._vertices:
                if not vertex.getVisited() and vertex._distance < min_dist:
                    min_dist = vertex._distance
                    current_vertex = vertex

            if current_vertex is None or current_vertex._distance == sys.maxsize:
                break # No path to remaining nodes

            current_vertex.setVisited()
            unvisited_count -= 1
            for neighbor, weight in current_vertex.getAdjacent():
                if not neighbor.getVisited(): #
                    new_dist = current_vertex._distance + weight
                    if new_dist < neighbor._distance:
                        neighbor._distance = new_dist
                        neighbor._predecessor = current_vertex

        # Reconstruct and print path
        if end_vertex._distance == sys.maxsize:
            print(f"No path found from '{start_label}' to '{end_label}'.", flush=True)
        else:
            path = DSALinkedList()
            current = end_vertex
            while current is not None:
                path.insertFirst(current.getLabel()) # Use insertFirst to build path
                current = current._predecessor
            
            path_str = ""
            for i, node_label in enumerate(path):
                path_str += node_label
                if i < len(path) - 1:
                    path_str += " -> "
            
            print(f"Path: {path_str}", flush=True)
            print(f"Total walking time: {end_vertex._distance} minutes.", flush=True)
        print("\n", flush=True)

def main():
    """
    test case
    All print output will be redirected to 'Assignment/output/1graph_results.txt'
    """
    output_dir = "output"
    output_file = os.path.join(output_dir, "1graph_results.txt")

    # This print() will go to the terminal *before* the redirect
    print(f"Starting graph tests... Output will be saved to {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        with redirect_stdout(f):

            print("#"*31, flush=True)
            print("###   Hospital Navigation   ###", flush=True)
            print("#"*31,"\n", flush=True)

            hospital_graph = DSAGraph()

            input_dir = "input"
            depts_file = os.path.join(input_dir, "departments.csv")
            corridors_file = os.path.join(input_dir, "corridors.csv")

            # Graph construction
            try:
                print(f"--- Phase 1: Building Graph from CSV files ---", flush=True)
                print(f"Reading departments from: {depts_file}", flush=True)
                with open(depts_file, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        hospital_graph.addVertex(row['department_name'])
                
                print(f"Reading corridors from: {corridors_file}", flush=True)
                with open(corridors_file, mode='r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        dept1 = row['department1']
                        dept2 = row['department2']
                        time = int(row['walking_time'])
                        hospital_graph.addEdge(dept1, dept2, time)
                
                print("Graph construction complete.", flush=True)

            except FileNotFoundError as e:
                print(f"ERROR: Could not find an input file: {e.filename}", flush=True)
                print("Please ensure 'departments.csv' and 'corridors.csv' are in the 'input' directory.", flush=True)
                return
            except Exception as e:
                print(f"An unexpected error occurred during file reading: {e}", flush=True)
                return
            
            # Display the constructed graph
            hospital_graph.displayAsList()
            hospital_graph.breadthFirstSearch("Emergency") # run BFS            
            hospital_graph.depthFirstSearchCycleFind() # Run DFS to find cycles

            
            hospital_graph.dijkstraAlgorithm("Emergency", "Outpatient Units") # Find and display a shortest path
            
            # Example with no path
            hospital_graph.dijkstraAlgorithm("Emergency", "Morgue")
            
            print("\n", flush=True)

    print(f"Graph tests complete. Results saved to {output_file}")


if __name__ == "__main__":
    main()

