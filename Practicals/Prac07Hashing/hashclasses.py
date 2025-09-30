import math
import csv

class DSAHashEntry: # Single box in the hash table. 
    # CONSTANTS for state of each slot in the hash table. 
    STATE_FREE = 0 # slot is alwyys empty. If we hit a a free slot we can stop because item isn't in the table. 
    STATE_USED = 1 # box is currently in use. Currently holds a key-value pair. 
    STATE_FORMERLY_USED = -1 # slot used to hold data but now removed. 

    def __init__(self, inputKey=None, inputValue=None):
        # CONSTRUCTOR
        if inputKey is not None: # if key and value is proided, create "USED" entry. 
            self.key = inputKey
            self.value = inputValue
            self.state = self.STATE_USED
        else: # if no data is provided -> create a "FREE" entry. 
            self.key = ""
            self.value = None
            self.state = self.STATE_FREE

class DSAHashTable:
    """Hash table itself."""
    STEP_HASH_MAX = 5 # Used in double hashing function to calcualte step size. 
    MAX_LOAD_FACTOR = 0.75 # if table gets more than 75% full, trigger resize to make it bigger. 
    MIN_LOAD_FACTOR = 0.25 # if table is less than 25% full, trigger resize to make it smaller and save memory. 
    INITIAL_CAPACITY = 11 # default starting size of table. 

    def __init__(self, tableSize=None):
        # CONSTRUCTOR
        if tableSize is None: # if no siz given, use default capacity. 
            tableSize = self.INITIAL_CAPACITY

        actualSize = self.find_next_prime(tableSize) # using next great prime number is a strategy to distribute keys more evenly. 
        self.hashArray = [DSAHashEntry() for s in range(actualSize)] # initialise hash array
        self.count = 0

    def put(self, in_key, in_value):
        if self.get_load_factor() >= self.MAX_LOAD_FACTOR:
            self.resize(self.getCapacity() * 2)
        
        in_key = str(in_key) # Ensure key is a string
        hashID = self.hash(in_key) # get the initial array index using main hash function
        step = self.stepHash(in_key) # get step size for probing using 2nd hash function
        
        initialPos = hashID
        i = 1
        is_new_entry = True

        # PROBING -
        while self.hashArray[hashID].state == DSAHashEntry.STATE_USED: # as long as current hash slot is being used. 
            if self.hashArray[hashID].key == in_key: # if keys match, just update to new value and stop. 
                self.hashArray[hashID].value = in_value
                is_new_entry = False
                break
            hashID = (initialPos + i * step) % self.getCapacity()
            i += 1 # probe jump to the next slot. 
            if hashID == initialPos: # if entire array was probed and we have returned to our start position. 
                raise OverflowError(f"Hash table is full. Cannot insert key '{in_key}'.")
        if is_new_entry: # if no matching keys were found: ,eans we found a free slot. 
            self.hashArray[hashID] = DSAHashEntry(in_key, in_value) # place new key-value pair
            self.count += 1

    def get(self, inputKey):
        inputKey = str(inputKey) # Ensure key is a string
        hashID = self.find(inputKey)
        if hashID == -1:
            raise KeyError(f"Key not found: {inputKey}")
        return self.hashArray[hashID].value

    def contains(self, in_key):
        in_key = str(in_key) # Ensure key is a string
        return self.find(in_key) != -1

    def remove(self, inputKey):
        inputKey = str(inputKey) # Ensure key is a string
        hashID = self.find(inputKey) 
        if hashID == -1:
            raise KeyError(f"Key not found: {inputKey}")

        value = self.hashArray[hashID].value
        self.hashArray[hashID].state = DSAHashEntry.STATE_FORMERLY_USED # instead of clearing slot immediately, mark as formerly used. 
        self.hashArray[hashID].key = ""
        self.hashArray[hashID].value = None
        self.count -= 1

        # after removing, check if table is now too empty. Shrink to save memory. 
        if self.getCapacity() > self.INITIAL_CAPACITY and self.get_load_factor() < self.MIN_LOAD_FACTOR:
             self.resize(self.getCapacity() // 2)
        return value

    def get_load_factor(self):
        return self.count / self.getCapacity() if self.getCapacity() > 0 else 0

    def getCapacity(self):
        return len(self.hashArray)

    def get_count(self):
        return self.count

    def display(self):
        print(f"--- Hash Table (Count: {self.count}, Capacity: {self.getCapacity()}) ---")
        for i, entry in enumerate(self.hashArray):
            print(f"[{i}]: ", end="")
            if entry.state == DSAHashEntry.STATE_USED:
                print(f"'{entry.key}' -> {entry.value}")
            elif entry.state == DSAHashEntry.STATE_FORMERLY_USED:
                print("<formerly used>")
            else:
                print("<free>")
        print("-------------------------------------")
    
    
    def load_from_csv(cls, filename):
        """
        Class method to load data from a CSV file into a new hash table.
        Assumes CSV format: id,name
        Args:
            filename (str): The path to the CSV file.
        Returns:
            A new DSAHashTable instance populated with the data.
        """
        # Read the file once to count the lines for initial sizing
        line_count = 0
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Skip header if it exists
            # next(reader, None) 
            for _ in reader:
                line_count += 1
        
        # Create a table sized appropriately for the data
        table = cls(int(line_count * 1.5)) # Start with some buffer
        
        print(f"Loading data from '{filename}' into a new hash table...")
        
        duplicates = 0
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    user_id, name = row[0], row[1]
                    if name in table:
                        duplicates += 1
                    # Use the name as the key and the ID as the value
                    table.put(name, user_id) 
        
        print(f"Load complete. {table.get_count()} unique entries loaded.")
        if duplicates > 0:
            print(f"Note: {duplicates} duplicate names were found and their ID values were updated.")
            
        return table

    def save2csv(self, filename):
        """
        Saves the contents of the hash table to a CSV file.
        Args:
            filename (str): The path for the output CSV file.
        """
        print(f"Saving hash table contents to '{filename}'...")
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name']) # Write header
            
            saved_count = 0
            # Iterate through the internal array and write used entries
            for entry in self.hashArray:
                if entry.state == DSAHashEntry.STATE_USED:
                    writer.writerow([entry.value, entry.key])
                    saved_count += 1
        
        print(f"Save complete. {saved_count} entries written to file.")

    def resize(self, new_size):
        old_array = self.hashArray
        new_capacity = self.find_next_prime(new_size)
        self.hashArray = [DSAHashEntry() for _ in range(new_capacity)]
        self.count = 0
        for entry in old_array:
            if entry.state == DSAHashEntry.STATE_USED:
                self.put(entry.key, entry.value)

    def find(self, in_key):
        hash_idx = self.hash(in_key)
        step = self.stepHash(in_key)
        initial_pos = hash_idx
        i = 1
        while self.hashArray[hash_idx].state != DSAHashEntry.STATE_FREE:
            if self.hashArray[hash_idx].state == DSAHashEntry.STATE_USED and \
               self.hashArray[hash_idx].key == in_key:
                return hash_idx
            hash_idx = (initial_pos + i * step) % self.getCapacity()
            i += 1
            if hash_idx == initial_pos:
                return -1
        return -1

    def hash(self, in_key):
        hash_idx = 0
        for char in in_key:
            hash_idx = (31 * hash_idx) + ord(char)
        return abs(hash_idx % self.getCapacity())

    def stepHash(self, in_key): # secondary hash function
        hash_val = self.hash(in_key)
        return self.STEP_HASH_MAX - (abs(hash_val) % self.STEP_HASH_MAX)

    def find_next_prime(self, start_val):
        if start_val <= 2: return 2
        prime_val = int(start_val)
        if prime_val % 2 == 0: prime_val += 1
        is_prime = False
        while not is_prime:
            is_prime = True
            i = 3
            while i * i <= prime_val:
                if prime_val % i == 0:
                    is_prime = False
                    break
                i += 2
            if not is_prime:
                prime_val += 2
        return prime_val

