class DSAHeapEntry:
    """
    Represents an entry in the heap, containing a priority and a value.
    """
    def __init__(self, priority, value):
        """
        Initializes a new heap entry.
        
        Args:
            priority (int): The priority of the entry.
            value (any): The value associated with the priority.
        """
        self._priority = priority
        self._value = value

    def get_priority(self):
        """Returns the priority of the entry."""
        return self._priority

    def set_priority(self, priority):
        """Sets the priority of the entry."""
        self._priority = priority

    def get_value(self):
        """Returns the value of the entry."""
        return self._value

    def set_value(self, value):
        """Sets the value of the entry."""
        self._value = value

    def __str__(self):
        """String representation for easy printing."""
        return f"({self._priority}, {self._value})"

    def __repr__(self):
        """Official string representation."""
        return str(self)
