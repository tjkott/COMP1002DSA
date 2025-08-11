class DSAStack:
    
    DEFAULT_CAPACITY = 100 
    def __init__(self, maxCapacity=None):
        """Default + alternate constructor combined."""
        if maxCapacity is None:
            capacity = self.DEFAULT_CAPACITY
        else:
            capacity = maxCapacity
        
        self.stack = [None] * capacity
        self.count = 0 
    
    # ACCESSORS
    def get_count(self):
        """ACCESSOR - Returns the number of items in the stack."""
        return self.count
    
    def isEmpty(self):
        """Checks if stack is empty"""
        return self.count == 0
    
    def isFull(self):
        """Checks if stack is full."""
        return self.count == len(self.stack)
    
   # MUTATORS
    def push(self, value):
        """ Adds an item to the top of the stack.
        Exception:
        Raises IndexError if stack is full.
        """
        if self.isFull():
            raise IndexError("Stack overflow - stack is full.")
        else:
            self.stack[self.count] = value
            self.count += 1
    
    def pop(self):
        """Takes the top mostitem from the stack."""
        topVal = self.top()
        self.count -= 1
        return topVal
    
    def top(self):
        """Looks at the top most item without removing it."""
        if self.isEmpty():
            raise IndexError("Stack is empty.")
        else:
            topVal = self.stack[self.count - 1]
            return topVal

class DSAQueue:
    """
    A class to represent a shuffling Queue data structure.
    """

    DEFAULT_CAPCITY = 100

    def __init__(self, maxCapacity=None):
        """Default + Alternate constructors combined."""
        if maxCapacity is None:
            capacity = self.DEFAULT_CAPCITY
        else:
            capacity = maxCapacity
        self.queue = [None]*capacity
        self.count = 0
    
    # ACCESSORS

    def getCount(self):
        """Returns the number of items in the queue."""
        return self.count
    
    def isEmpty(self):
        """Checks if the the queue is empty."""
        return self.count == 0
    
    def isFull(self):
        """Cehks if queue is full."""
        return self.count == len(self.queue)
    
    def peek(self):
        """Checks the front item but doesn't take it off."""
        if self.isEmpty():
            raise IndexError("Queue is empty.")
        else:
            frontVal = self.queue[0]
            return frontVal
    
    # MUTATORS

    def enqueue(self, value):
        """Adds items to the queue at the end"""
        if self.isFull(): # Exception
            raise IndexError("Queue overflow - queue is full.")
        else:
            self.queue[self.count] = value
            self.count += 1
    
    def dequeue(self):
        """Take item from the front of the queue"""
        frontVal  = self.peek() # use peek() method to get the current value at the front of the queue
        self.count -= 1
        
        for i in range(self.count):# shuffle all elements to the left. 
            self.queue[i] = self.queue[i + 1]

        
        return frontVal

if __name__ == '__main__':
    print("--- Testing DSAStack ---")
    # Using alternate constructor
    stack = DSAStack()
    print(f"Is stack empty? {stack.isEmpty()}")

    print("\nPushing items: 10, 'hello', 3.14")
    stack.push(10)
    stack.push("hello")
    stack.push(3.14)

    print(f"Stack count: {stack.get_count()}")
    print(f"Is stack full? {stack.isFull()}")
    print(f"Top item: {stack.top()}")

    print("\nPopping an item...")
    popped_item = stack.pop()
    print(f"Popped: {popped_item}")
    print(f"New top item: {stack.top()}")
    print(f"Stack count: {stack.get_count()}")

    print("\n" + "="*40 + "\n")

    print("--- Testing DSAQueue (Shuffling, following pseudocode) ---")
    # Using default constructor
    queue = DSAQueue()
    print(f"Is queue empty? {queue.isEmpty()}")

    print("\nEnqueuing items: 'A', 'B', 'C'")
    queue.enqueue('A')
    queue.enqueue('B')
    queue.enqueue('C')

    print(f"Queue count: {queue.getCount()}")
    print(f"Is queue full? {queue.isFull()}")
    print(f"Front item: {queue.peek()}")

    print("\nDequeuing an item...")
    dequeued_item = queue.dequeue()
    print(f"Dequeued: {dequeued_item}")
    print(f"New front item: {queue.peek()}")
    print(f"Queue count: {queue.getCount()}")

    print("\nEnqueuing another item: 'D'")
    queue.enqueue('D')
    print("Dequeuing again...")
    queue.dequeue()
    print(f"New front item: {queue.peek()}")
    print(f"Current queue count: {queue.getCount()}")
