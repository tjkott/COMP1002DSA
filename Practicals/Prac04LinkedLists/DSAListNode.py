class DSAListNode:
    """
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