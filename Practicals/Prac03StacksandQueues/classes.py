# Author: Thejana Kottawatta Hewage (22307822)
# Data Structures and Algorithms COMP1002
# 
# classes.py - Python file to hold stack and queue classes. 
#

class DSAStack:
    DEFAULT_CAPACITY = 100 
    def __init__(self, maxCapacity=None):
        """Default + alternate constructor combined."""
        if maxCapacity is None:
            capacity = self.DEFAULT_CAPACITY
        else:
            capacity = maxCapacity
        
        self.stack = [None] * capacity # a standard python list. Can successfully hold references to any type of object.
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

class DSAQueue(object): # Parent queue class
    """
    A class to represent a shuffling Queue data structure.
    """

    DEFAULT_CAPACITY = 100

    def __init__(self, maxCapacity=None):
        """Default + Alternate constructors combined."""
        if maxCapacity is None:
            capacity = self.DEFAULT_CAPACITY
        else:
            capacity = maxCapacity
        self.queue = [None]*capacity # a standard python list. Can successfully hold references to any type of object.
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
    
    # MUTATORS - to be implemented by sub-classes. 
    def enqueue(self, value):
        # To be implemented by sub-clases.
        raise NotImplementedError("enqueue() to be implemented in sub-class")

    def dequeue(self):
        raise NotImplementedError("dequeue() to be implemented in sub-class")
    
    def peek(self):
        raise NotImplementedError("peek() to be implemented in sub-class")

class DSAShufflingQueue(DSAQueue):
    """
    Shuffling implementation of DSAQueue
    """

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
    
    def peek(self):
        """Checks the front item but doesn't take it off."""
        if self.isEmpty():
            raise IndexError("Queue is empty.")
        else:
            frontVal = self.queue[0]
            return frontVal

class DSACircularQueue(DSAQueue):
    """
    A class to represent circular queue data structure.
    More efficient that shuffling queue but trickier to code.
    """
    def __init__(self, maxCapacity=None):
        super(DSACircularQueue, self).__init__(maxCapacity)
        self.front = 0
    
    def enqueue(self, value):
        """Adds an item to the end of the queue."""
        if self.isFull():
            raise IndexError("Queue overflow: queue is full.")
        else:
            # Rear index for wraparound. 
            rear = (self.front + self.count) % len(self.queue)
            self.queue[rear] = value
            self.count += 1
    
    def dequeue(self):
        """Removes and returns the front item from the queue."""
        if self.isEmpty(): # exception
            raise IndexError("Queue underflow: queue is empty.")
        frontVal = self.queue[self.front] # value of the front of the queue
        # shift the front pointer forwards. 
        self.front = (self.front + 1) % len(self.queue)
        self.count -= 1
        return frontVal
    
    def peek(self):
        """Returns the front item without removing it."""
        if self.isEmpty(): # exception
            raise IndexError("Queue underflow: queue is empty.")
        return self.queue[self.front]

# Mini demo
if __name__ == '__main__':
    print("--- Testing DSAStack ---")
    stack = DSAStack(maxCapacity=5)
    stack.push(10)
    stack.push("hello")
    print(f"Stack Top: {stack.top()}")
    print(f"Popped: {stack.pop()}")
    print(f"Stack Count: {stack.get_count()}")

    print("\n" + "="*40 + "\n")

    print("--- Testing DSAShufflingQueue ---")
    s_queue = DSAShufflingQueue(maxCapacity=5)
    s_queue.enqueue('A')
    s_queue.enqueue('B')
    print(f"Shuffling Queue Front: {s_queue.peek()}")
    print(f"Dequeued: {s_queue.dequeue()}")
    print(f"New Front: {s_queue.peek()}")
    print(f"Shuffling Queue Count: {s_queue.getCount()}")

    print("\n" + "="*40 + "\n")

    print("--- Testing DSACircularQueue ---")
    c_queue = DSACircularQueue(maxCapacity=5)
    print(f"Is circular queue empty? {c_queue.isEmpty()}")

    print("\nEnqueuing items: 1, 2, 3, 4, 5 (to fill the queue)")
    for i in range(1, 6):
        c_queue.enqueue(i)

    print(f"Is circular queue full? {c_queue.isFull()}")
    print(f"Front item: {c_queue.peek()}")

    print("\nDequeuing two items...")
    print(f"Dequeued: {c_queue.dequeue()}")
    print(f"Dequeued: {c_queue.dequeue()}")
    print(f"New front item: {c_queue.peek()}")
    print(f"Queue count: {c_queue.getCount()}")

    print("\nEnqueuing two more items (6, 7) to demonstrate wrap-around...")
    c_queue.enqueue(6)
    c_queue.enqueue(7)

    print(f"Front item is still: {c_queue.peek()}")
    print("Dequeuing all remaining items to see the order:")
    while not c_queue.isEmpty():
        print(f"Dequeued: {c_queue.dequeue()}")
