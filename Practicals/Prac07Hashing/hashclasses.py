import math
import csv

class DSAHashEntry: # Single box in the hash table. 
    # CONSTANTS for state of each slot in the hash table. 
    STATE_FREE = 0 # slot is alwyys empty. If we hit a a free slot we can stop because item isn't in the table. 
    STATE_USED = 1 # box is currently in use. Currently holds a key-value pair. 
    STATE_FORMERLY_USED = -1 # slot used to hold data but now removed. 

    def __init__(self, in_key=None, in_value=None):
        # CONSTRUCTOR
        if in_key is not None: # if key and value is proided, create "USED" entry. 
            self.key = in_key
            self.value = in_value
            self.state = self.STATE_USED
        else: # if no data is provided -> create a "FREE" entry. 
            self.key = ""
            self.value = None
            self.state = self.STATE_FREE


# Implements a hash table data structure with 
# The implementation follows the structure and guidelines from the provided lecture materials.
class DSAHashTable:
    _STEP_HASH_MAX = 5
    _MAX_LOAD_FACTOR = 0.75
    _MIN_LOAD_FACTOR = 0.25
    _INITIAL_CAPACITY = 11

    def __init__(self, table_size=None):
        if table_size is None:
            table_size = self._INITIAL_CAPACITY
        actual_size = self._find_next_prime(table_size)
        self.hash_array = [DSAHashEntry() for _ in range(actual_size)]
        self.count = 0

    def put(self, in_key, in_value):
        if self.get_load_factor() >= self._MAX_LOAD_FACTOR:
            self._resize(self.get_capacity() * 2)
        
        in_key = str(in_key) # Ensure key is a string
        hash_idx = self._hash(in_key)
        step = self._step_hash(in_key)
        
        initial_pos = hash_idx
        i = 1
        is_new_entry = True

        while self.hash_array[hash_idx].state == DSAHashEntry.STATE_USED:
            if self.hash_array[hash_idx].key == in_key:
                self.hash_array[hash_idx].value = in_value
                is_new_entry = False
                break
            hash_idx = (initial_pos + i * step) % self.get_capacity()
            i += 1
            if hash_idx == initial_pos:
                raise OverflowError(f"Hash table is full. Cannot insert key '{in_key}'.")

        if is_new_entry:
            self.hash_array[hash_idx] = DSAHashEntry(in_key, in_value)
            self.count += 1

    def get(self, in_key):
        in_key = str(in_key) # Ensure key is a string
        hash_idx = self._find(in_key)
        if hash_idx == -1:
            raise KeyError(f"Key not found: {in_key}")
        return self.hash_array[hash_idx].value

    def __contains__(self, in_key):
        in_key = str(in_key) # Ensure key is a string
        return self._find(in_key) != -1

    def remove(self, in_key):
        in_key = str(in_key) # Ensure key is a string
        hash_idx = self._find(in_key)
        if hash_idx == -1:
            raise KeyError(f"Key not found: {in_key}")

        value = self.hash_array[hash_idx].value
        self.hash_array[hash_idx].state = DSAHashEntry.STATE_FORMERLY_USED
        self.hash_array[hash_idx].key = ""
        self.hash_array[hash_idx].value = None
        self.count -= 1

        if self.get_capacity() > self._INITIAL_CAPACITY and self.get_load_factor() < self._MIN_LOAD_FACTOR:
             self._resize(self.get_capacity() // 2)
        return value

    def get_load_factor(self):
        return self.count / self.get_capacity() if self.get_capacity() > 0 else 0

    def get_capacity(self):
        return len(self.hash_array)

    def get_count(self):
        return self.count

    def display(self):
        print(f"--- Hash Table (Count: {self.count}, Capacity: {self.get_capacity()}) ---")
        for i, entry in enumerate(self.hash_array):
            print(f"[{i}]: ", end="")
            if entry.state == DSAHashEntry.STATE_USED:
                print(f"'{entry.key}' -> {entry.value}")
            elif entry.state == DSAHashEntry.STATE_FORMERLY_USED:
                print("<formerly used>")
            else:
                print("<free>")
        print("-------------------------------------")
    
    @classmethod
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

    def save_to_csv(self, filename):
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
            for entry in self.hash_array:
                if entry.state == DSAHashEntry.STATE_USED:
                    writer.writerow([entry.value, entry.key])
                    saved_count += 1
        
        print(f"Save complete. {saved_count} entries written to file.")

    def _resize(self, new_size):
        old_array = self.hash_array
        new_capacity = self._find_next_prime(new_size)
        self.hash_array = [DSAHashEntry() for _ in range(new_capacity)]
        self.count = 0
        for entry in old_array:
            if entry.state == DSAHashEntry.STATE_USED:
                self.put(entry.key, entry.value)

    def _find(self, in_key):
        hash_idx = self._hash(in_key)
        step = self._step_hash(in_key)
        initial_pos = hash_idx
        i = 1
        while self.hash_array[hash_idx].state != DSAHashEntry.STATE_FREE:
            if self.hash_array[hash_idx].state == DSAHashEntry.STATE_USED and \
               self.hash_array[hash_idx].key == in_key:
                return hash_idx
            hash_idx = (initial_pos + i * step) % self.get_capacity()
            i += 1
            if hash_idx == initial_pos:
                return -1
        return -1

    def _hash(self, in_key):
        hash_idx = 0
        for char in in_key:
            hash_idx = (31 * hash_idx) + ord(char)
        return abs(hash_idx % self.get_capacity())

    def _step_hash(self, in_key):
        hash_val = self._hash(in_key)
        return self._STEP_HASH_MAX - (abs(hash_val) % self._STEP_HASH_MAX)

    def _find_next_prime(self, start_val):
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

