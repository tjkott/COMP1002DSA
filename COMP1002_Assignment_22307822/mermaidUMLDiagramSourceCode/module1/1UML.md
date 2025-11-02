```mermaid
classDiagram
direction LR
    class DSAListNode {
	    +value: any
	    +next: DSAListNode
	    +__init__(value)
    }

    class DSALinkedList {
	    -head: DSAListNode
	    -count: int
	    +__init__()
	    +insertLast(value)
	    +removeFirst() : any
	    +isEmpty() : bool
	    +__iter__()
	    +__len__() : int
    }

    class DSAQueue {
	    -_list: DSALinkedList
	    +__init__()
	    +enqueue(value)
	    +dequeue() : any
	    +isEmpty() : bool
    }

    class DSAGraph {
	    -_vertices: DSALinkedList
	    +__init__()
	    +addVertex(label)
	    +addEdge(label1, label2, weight)
	    +getVertex(label) : DSAGraphVertex
	    +hasVertex(label) : bool
	    +ClearAllVisited()
	    +displayAsList()
	    +breadthFirstSearch(start_label)
	    +depthFirstSearchCycleFind()
	    +DfsCycleHelper(vertex, visited, recursionstack) : list
	    +dijkstraAlgorithm(start_label, end_label)
    }

    class DSAGraphVertex {
	    +label: string
	    +links: DSALinkedList
	    +visited: bool
	    +distance: int
	    +predecessor: DSAGraphVertex
	    +__init__(label)
	    +getLabel() : string
	    +getAdjacent() : DSALinkedList
	    +addEdge(neighbor_vertex, weight)
	    +setVisited()
	    +clearVisited()
	    +getVisited() : bool
	    +__str__() : string
    }

    DSALinkedList -- DSAListNode : contains
    DSAQueue -- DSALinkedList : uses
    DSAGraph -- DSALinkedList : stores vertices in
    DSAGraphVertex -- DSALinkedList : stores edges in
    DSAGraph -- DSAGraphVertex : aggregates


