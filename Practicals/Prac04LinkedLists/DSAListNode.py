class DSAListNode:
    """
    A ListNode for singly-linked list.
    Container for data value and next reference.
    """
    # constructor
    def __init__(self, inValue):
        self.value =   inValue
        self.next = None
    
    def getValue(self): #accessor
        # returns node's stores value. 
        return self.value
    
    def setValue(self, inValue): #mutator
        # Updates the values of the node. 
        self.value = inValue

    def getNext(self): #accessor
        # REturns the references to the next ndoe in the lsit. 
        return self.next
    
    def setNext(self, newNext): #mutator
        # Updates the node's next pointer to a enw code. 
        self.next = newNext
    
    def getPrev(self):
        # Return reference to the previous node in the list. 
        return self.prev
    
    def setPrev(self, newPrev):
        # Update the node's previous pointer to a new node. 
        self.prev = newPrev

class DSADoublyLinkedList:
    """
    A Doubly-Linked, Double-Ended Linked List.
    Maintains references to both the head and tail nodes for efficient
    operations at both ends of the list.
    """
    def __init__(self):
        # Default contructor
        self.head = None
        self.tail = None
        self.count = 0

    def __iter__(self):
        """Iterator to allow looping over the list's values."""
        curr = self.head
        while curr is not None:
            yield curr.getValue()
            curr = curr.getNext()

    def __str__(self):
        """Returns a string representation of the list."""
        return " -> ".join(str(v) for v in self)

    def getCount(self):
        """Returns the number of items in the list."""
        return self.count

    def isEmpty(self):
        """Checks if the list is empty."""
        return self.head is None

    def insertFirst(self, newValue):
        """
        Inserts a new node at the beginning of the list.
        Handles three cases:
        (a) Empty list: head and tail point to the new node.
        (b/c) Non-empty list: new node becomes the new head.
        """
        newNd = DSAListNode(newValue)
        if self.isEmpty():
            # Case (a): List is empty
            self.head = newNd
            self.tail = newNd
        else:
            # Case (b/c): List has one or more items
            newNd.setNext(self.head)
            self.head.setPrev(newNd)
            self.head = newNd
        self.count += 1

    def insertLast(self, newValue):
        """
        Inserts a new node at the end of the list.
        Handles three cases:
        (a) Empty list: head and tail point to the new node.
        (b/c) Non-empty list: new node becomes the new tail.
        """
        newNd = DSAListNode(newValue)
        if self.isEmpty():
            # Case (a): List is empty
            self.head = newNd
            self.tail = newNd
        else:
            # Case (b/c): List has one or more items
            self.tail.setNext(newNd)
            newNd.setPrev(self.tail)
            self.tail = newNd
        self.count += 1

    def peekFirst(self):
        # Returns the value of the first node without removing it.
        if self.isEmpty():
            # raise exception is list is empty
            raise IndexError("Cannot peek at an empty list.") 
        return self.head.getValue()

    def peekLast(self):
        # Returns the value of the last node without removing it.
        if self.isEmpty():
            raise IndexError("Cannot peek at an empty list.")
        return self.tail.getValue()

    def removeFirst(self):
        """
        Removes the first node and returns its value.
        Handles three cases:
        (a) Empty list: raises an exception.
        (b) One-item list: list becomes empty.
        (c) Multi-item list: head pointer moves to the next node.
        """
        if self.isEmpty():
            # Case (a): Cannot remove from an empty list
            raise IndexError("Cannot remove from an empty list.")
        
        nodeValue = self.head.getValue()
        if self.head is self.tail:
            # Case (b): Only one item in the list
            self.head = None
            self.tail = None
        else:
            # Case (c): More than one item in the list
            self.head = self.head.getNext()
            self.head.setPrev(None) # The new head has no previous node
        self.count -= 1
        return nodeValue

    def removeLast(self):
        """
        Removes the last node and returns its value.
        Handles three cases:
        (a) Empty list: raises an exception.
        (b) One-item list: list becomes empty.
        (c) Multi-item list: tail pointer moves to the previous node.
        """
        if self.isEmpty():
            # Case (a): Cannot remove from an empty list
            raise IndexError("Cannot remove from an empty list.")

        nodeValue = self.tail.getValue()
        if self.head is self.tail:
            # Case (b): Only one item in the list
            self.head = None
            self.tail = None
        else:
            # Case (c): More than one item in the list
            self.tail = self.tail.getPrev()
            self.tail.setNext(None) # The new tail has no next node
        self.count -= 1
        return nodeValue

# --- Interactive Menu for DSALinkedList ---
def interactive_linked_list_menu():
    """Provides an interactive menu to explore the operations in a Linked List."""
    linked_list = DSADoublyLinkedList()
    
    while True:
        print("\n--- Linked List Operations Menu ---")
        print("(a) InsertFirst / InsertLast")
        print("(b) RemoveFirst / RemoveLast")
        print("(c) Display the list")
        print("---------------------------------")
        print("1. Insert First")
        print("2. Insert Last")
        print("3. Remove First")
        print("4. Remove Last")
        print("5. Display List")
        print("6. Get Count")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            value = input("Enter value to insert first: ")
            linked_list.insertFirst(value)
            print(f"'{value}' inserted. List: {linked_list}")
        elif choice == '2':
            value = input("Enter value to insert last: ")
            linked_list.insertLast(value)
            print(f"'{value}' inserted. List: {linked_list}")
        elif choice == '3':
            try:
                value = linked_list.removeFirst()
                print(f"Removed '{value}'. List: {linked_list}")
            except IndexError as e:
                print(f"Error: {e}")
        elif choice == '4':
            try:
                value = linked_list.removeLast()
                print(f"Removed '{value}'. List: {linked_list}")
            except IndexError as e:
                print(f"Error: {e}")
        elif choice == '5':
            print(f"Current list: {linked_list}")
        elif choice == '6':
            print(f"List count: {linked_list.getCount()}")
        elif choice == '0':
            print("Exiting linked list menu.")
            return
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # This menu runs if you execute linked_list.py directly
    interactive_linked_list_menu()
